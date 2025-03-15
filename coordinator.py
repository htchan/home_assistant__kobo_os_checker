"""Data update coordinator for Version entities."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    LOGGER,
    DOMAIN, 
    UPDATE_COORDINATOR_UPDATE_INTERVAL,
    KOBO_DEVICE_ID_MAPPING,
)

import requests
import re
from datetime import datetime
from zoneinfo import ZoneInfo
import asyncio

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
    
    def fetch_data(self) -> dict:
        """Fetch data from Kobo API."""
        try:
            resp = requests.get(f'http://api.kobobooks.com/1.0/UpgradeCheck/Device/{self.device_id}/kobo/0.0/N0')
            resp.raise_for_status()
            data = resp.json()
            result = re.search(r'https://ereaderfiles.kobo.com/firmwares/(.*?)/(.*?)/kobo-update-(.*?).zip', data['UpgradeURL'])
            return {
                'version': f"{result.group(1)} - {result.group(3)}",
                'date': datetime.strptime(result.group(2), "%b%Y").replace(tzinfo=ZoneInfo('UTC')),
                "release_note_url": data['ReleaseNoteURL']
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    async def _async_update_data(self) -> dict:
        """Fetch data from Kobo API."""
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self.fetch_data)
        
        return result