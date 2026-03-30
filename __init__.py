"""The Kobo OS Checker integration."""

from datetime import timedelta

from .coordinator import KoboOsDataUpdateCoordinator
from .const import (
    CONF_KOBO_DEVICE,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
    PLATFORMS,
)


async def async_setup_entry(hass, entry):
    """Set up the sensor from a config entry."""
    update_minutes = entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)

    coordinator = KoboOsDataUpdateCoordinator(
        hass,
        entry,
        device_name=entry.data[CONF_KOBO_DEVICE],
        update_interval=timedelta(minutes=update_minutes),
    )
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
