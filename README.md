# Home Assistant - Kobo OS Checker Integration

This integration fetches data from `api.kobobooks.com` to check the latest OS release version of a specific Kobo device.

## Installation

### Via HACS (recommended)
1. Open HACS → Integrations → ⋮ → Custom repositories
2. Add `https://github.com/htchan/home_assistant__kobo_os_checker` as category **Integration**
3. Install "Kobo OS Checker" and restart Home Assistant

### Manual
Clone or copy this repo into `config/custom_components/home_assistant__kobo_os_checker/`.

## Entities

For each configured device, three sensors are created:

| Entity ID | Description |
|---|---|
| `sensor.{device_name}__os_version` | Latest firmware version |
| `sensor.{device_name}__os_release_date` | Firmware release date |
| `sensor.{device_name}__os_release_note_url` | Link to release notes |

The update interval is 6 hours (360 minutes).

## Supported Kobo Devices

- Kobo Touch A/B
- Kobo Touch C
- Kobo Mini
- Kobo Glo
- Kobo Glo HD
- Kobo Touch 2.0
- Kobo Aura
- Kobo Aura HD
- Kobo Aura H2O
- Kobo Aura H2O Edition 2 v1
- Kobo Aura H2O Edition 2 v2
- Kobo Aura ONE
- Kobo Aura ONE Limited Edition
- Kobo Aura Edition 2 v1
- Kobo Aura Edition 2 v2
- Kobo Nia
- Kobo Clara HD
- Kobo Forma
- Kobo Libra H2O
- Kobo Elipsa
- Kobo Sage
- Kobo Libra 2
- Kobo Clara 2E
- Kobo Elipsa 2E
- Kobo Libra Colour
- Kobo Clara BW
- Kobo Clara Colour
