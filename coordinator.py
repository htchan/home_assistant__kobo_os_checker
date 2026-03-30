"""Data update coordinator for Kobo OS Checker entities."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    LOGGER,
    DOMAIN,
    UPDATE_COORDINATOR_UPDATE_INTERVAL,
    KOBO_DEVICE_ID_MAPPING,
)

import aiohttp
import re
from datetime import datetime
from zoneinfo import ZoneInfo

API_BASE_URL = "https://api.kobobooks.com/1.0/UpgradeCheck/Device"
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=30)
MAX_RESPONSE_SIZE = 1024 * 1024  # 1 MB


class KoboOsDataUpdateCoordinator(DataUpdateCoordinator[dict]):
    """Data update coordinator for Kobo OS entities."""

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        device_name: str,
        update_interval: timedelta = UPDATE_COORDINATOR_UPDATE_INTERVAL,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self.device_name = device_name
        self.device_id = KOBO_DEVICE_ID_MAPPING[device_name]
        self.config_entry = config_entry

    async def _async_update_data(self) -> dict:
        """Fetch data from Kobo API."""
        session = async_get_clientsession(self.hass)
        url = f"{API_BASE_URL}/{self.device_id}/kobo/0.0/N0"

        try:
            async with session.get(url, timeout=REQUEST_TIMEOUT) as resp:
                resp.raise_for_status()

                # Validate content type
                content_type = resp.headers.get("Content-Type", "")
                if "json" not in content_type and "text" not in content_type:
                    raise UpdateFailed(
                        f"Unexpected content type from API: {content_type}"
                    )

                # Guard against oversized responses
                content_length = resp.content_length
                if content_length and content_length > MAX_RESPONSE_SIZE:
                    raise UpdateFailed(
                        f"API response too large: {content_length} bytes"
                    )

                data = await resp.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except TimeoutError as err:
            raise UpdateFailed(f"Timeout fetching firmware data: {err}") from err

        if not isinstance(data, dict):
            raise UpdateFailed(f"Unexpected API response type: {type(data).__name__}")

        upgrade_url = data.get("UpgradeURL")
        if not upgrade_url:
            raise UpdateFailed("UpgradeURL not found in API response")

        if not isinstance(upgrade_url, str):
            raise UpdateFailed(f"UpgradeURL is not a string: {type(upgrade_url).__name__}")

        result = re.search(
            r"https://ereaderfiles\.kobo\.com/firmwares/(.*?)/(.*?)/kobo-update-(.*?)\.zip",
            upgrade_url,
        )
        if not result:
            raise UpdateFailed(f"Could not parse firmware URL: {upgrade_url}")

        return {
            "version": f"{result.group(1)} - {result.group(3)}",
            "date": datetime.strptime(result.group(2), "%b%Y").replace(
                tzinfo=ZoneInfo("UTC")
            ),
            "release_note_url": data.get("ReleaseNoteURL", ""),
        }
