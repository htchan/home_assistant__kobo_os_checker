from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

import voluptuous as vol

from .const import (
    DOMAIN,
    DEFAULT_CONFIG,
    STEP_USER,
    CONF_KOBO_DEVICE,
    CONF_UPDATE_INTERVAL,
    DEFAULT_KOBO_DEVICE,
    DEFAULT_UPDATE_INTERVAL,
    KOBO_DEVICE_ID_MAPPING,
)


class KoboOsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Kobo OS Version."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the Version config flow."""
        self._entry_data: dict[str, Any] = DEFAULT_CONFIG.copy()

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle the initial user step."""
        if user_input is not None:
            # Check for duplicate device
            self._async_abort_entries_match(
                {CONF_KOBO_DEVICE: user_input[CONF_KOBO_DEVICE]}
            )
            self._entry_data.update(user_input)
            return self.async_create_entry(
                title=self._entry_data[CONF_KOBO_DEVICE],
                data=self._entry_data,
            )

        self._entry_data = DEFAULT_CONFIG.copy()
        return self.async_show_form(
            step_id=STEP_USER,
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_KOBO_DEVICE,
                        default=DEFAULT_KOBO_DEVICE,
                    ): vol.In(KOBO_DEVICE_ID_MAPPING.keys()),
                    vol.Optional(
                        CONF_UPDATE_INTERVAL,
                        default=DEFAULT_UPDATE_INTERVAL,
                    ): vol.All(vol.Coerce(int), vol.Range(min=60, max=1440)),
                }
            ),
        )
