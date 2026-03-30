"""Common entity class for Kobo OS Checker integration."""

from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import KoboOsDataUpdateCoordinator


class KoboOsEntity(CoordinatorEntity[KoboOsDataUpdateCoordinator]):
    """Common entity class for Kobo OS Checker integration."""

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
            manufacturer="Rakuten Kobo",
            entry_type=DeviceEntryType.SERVICE,
        )
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        )
