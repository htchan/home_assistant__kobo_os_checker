"""Data update coordinator for Version entities."""

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

import re
from datetime import datetime
from zoneinfo import ZoneInfo


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
        url = f"http://api.kobobooks.com/1.0/UpgradeCheck/Device/{self.device_id}/kobo/0.0/N0"

        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                data = await resp.json()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

        upgrade_url = data.get("UpgradeURL")
        if not upgrade_url:
            raise UpdateFailed("UpgradeURL not found in API response")

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
