"""Common entity class for Version integration."""

from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import KoboOsDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up kobo os sensors."""
    coordinator = entry.runtime_data
    if (entity_name := entry.data[CONF_NAME]) == DEFAULT_NAME:
        entity_name = entry.title

    version_sensor_entities: list[VersionSensorEntity] = [
        KoboOsEntity(
            coordinator=coordinator,
            entity_description=SensorEntityDescription(
                key=str(entry.data[CONF_KOBO_DEVICE]),
                name=entity_name,
                translation_key="kobo_os",
            ),
        )
    ]

    async_add_entities(version_sensor_entities)

class KoboOsEntity(CoordinatorEntity[KoboOsDataUpdateCoordinator]):
    """Common entity class for Version integration."""

    def __init__(
        self,
        coordinator: KoboOsDataUpdateCoordinator,
        entity_description: EntityDescription,
    ) -> None:
        """Initialize version entities."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            name=f"{coordinator.device_name}",
            identifiers={(DOMAIN, coordinator.device_id)},
            manufacturer="htchan",
            entry_type=DeviceEntryType.SERVICE,
        )
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        )