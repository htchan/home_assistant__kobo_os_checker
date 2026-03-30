"""Sensor platform for Kobo OS Checker integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_KOBO_DEVICE
from .coordinator import KoboOsDataUpdateCoordinator
from .entity import KoboOsEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensors."""
    entity_name = entry.data.get(CONF_NAME) or entry.title
    coordinator: KoboOsDataUpdateCoordinator = entry.runtime_data
    async_add_entities(
        [
            KoboOsVersionSensor(
                entry=entry,
                coordinator=coordinator,
                entity_description=SensorEntityDescription(
                    key=f"{entry.data[CONF_KOBO_DEVICE]}_version",
                    name=entity_name,
                    translation_key="kobo_os_version",
                ),
            ),
            KoboOsReleaseDateSensor(
                entry=entry,
                coordinator=coordinator,
                entity_description=SensorEntityDescription(
                    key=f"{entry.data[CONF_KOBO_DEVICE]}_date",
                    device_class=SensorDeviceClass.TIMESTAMP,
                    name=entity_name,
                    translation_key="kobo_os_date",
                ),
            ),
            KoboOsReleaseNoteUrlSensor(
                entry=entry,
                coordinator=coordinator,
                entity_description=SensorEntityDescription(
                    key=f"{entry.data[CONF_KOBO_DEVICE]}_release_note_url",
                    name=entity_name,
                    translation_key="kobo_os_release_note_url",
                ),
            ),
        ]
    )


class KoboOsVersionSensor(KoboOsEntity, SensorEntity):
    """Sensor for Kobo OS version."""

    _attr_name = "Kobo OS Version"

    def __init__(self, entry: ConfigEntry, coordinator: KoboOsDataUpdateCoordinator, entity_description: SensorEntityDescription) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator=coordinator, entity_description=entity_description)
        self._attr_unique_id = f"{DOMAIN}__{coordinator.device_name}__os_version"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data.get("version") if self.coordinator.data else None


class KoboOsReleaseDateSensor(KoboOsEntity, SensorEntity):
    """Sensor for Kobo OS date."""

    _attr_name = "Kobo OS Date"

    def __init__(self, entry: ConfigEntry, coordinator: KoboOsDataUpdateCoordinator, entity_description: SensorEntityDescription) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator=coordinator, entity_description=entity_description)
        self._attr_unique_id = f"{DOMAIN}__{coordinator.device_name}__os_release_date"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data.get("date") if self.coordinator.data else None


class KoboOsReleaseNoteUrlSensor(KoboOsEntity, SensorEntity):
    """Sensor for Kobo OS release note URL."""

    _attr_name = "Kobo OS Release Note URL"

    def __init__(self, entry: ConfigEntry, coordinator: KoboOsDataUpdateCoordinator, entity_description: SensorEntityDescription) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator=coordinator, entity_description=entity_description)
        self._attr_unique_id = f"{DOMAIN}__{coordinator.device_name}__os_release_note_url"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data.get("release_note_url") if self.coordinator.data else None
