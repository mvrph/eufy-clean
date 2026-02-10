# Eufy Clean

Home Assistant custom integration for controlling Eufy robot vacuums over MQTT. Built for the **Robovac X10 Pro Omni**, but compatible with other MQTT-enabled Eufy vacuums. Can also be used as a standalone Python library without Home Assistant.

Forked from [martijnpoppen/eufy-clean](https://github.com/martijnpoppen/eufy-clean) and rewritten in Python with Home Assistant support.

## Features

- Cloud login and device pairing via the Eufy API
- Real-time vacuum control over MQTT
- Home Assistant config flow for easy setup
- Scene cleaning and room-specific cleaning
- Battery level sensor (useful for off-peak charging schedules)
- Standalone Python usage — no Home Assistant required

## Requirements

- Python 3.12+
- An MQTT-enabled Eufy vacuum (e.g. Robovac X10 Pro Omni)
- Home Assistant (optional — the library works standalone)

## Installation

### Home Assistant (HACS)

1. Add this repository to [HACS](https://hacs.xyz/) as a custom integration.
2. Install **Eufy Robovac MQTT**.
3. Restart Home Assistant.
4. Go to **Settings > Devices & Services > Add Integration** and search for "Eufy Robovac MQTT".
5. Log in with your Eufy app credentials.

### Standalone Python

```bash
git clone https://github.com/mvrph/eufy-clean.git
cd eufy-clean
pip install -r requirements-standalone.txt
```

For standalone usage you only need the lightweight dependencies listed in `requirements-standalone.txt`. The full `requirements.txt` includes Home Assistant and is only needed for integration development.

## Usage

### Home Assistant Services

#### Scene Cleaning

```yaml
action: vacuum.send_command
data:
  command: scene_clean
  params:
    scene: 5
target:
  entity_id: vacuum.robovac_x10_pro_omni
```

**Scene numbers:**

| Scene | Description |
|-------|-------------|
| 1     | Full home daily clean |
| 2     | Full home deep clean |
| 3     | Post-meal clean |
| 4+    | Custom scenes, in the order you created them in the Eufy app |

#### Room Cleaning

```yaml
action: vacuum.send_command
data:
  command: room_clean
  map_id: 4
  params:
    rooms:
      - 3
      - 4
target:
  entity_id: vacuum.robovac_x10_pro_omni
```

Room IDs are assigned by mapping order — starting from the room left of the base station and incrementing. The base station room is last. You can verify IDs by testing `vacuum.room_clean` and checking the Eufy app.

> [!TIP]
> If you get "Unable to identify position", your default `map_id` is likely higher than expected (this happens when you've had multiple maps). Try incrementing — 20 is not an unusual number.

#### Battery Sensor

The integration exposes a battery charge sensor in Home Assistant, useful for tracking charge level and scheduling off-peak charging.

![Battery sensor in Home Assistant](assets/eufy-battery.png)

### Standalone Python

Set your Eufy credentials in a `.env` file:

```
EUFY_USERNAME=your-email@example.com
EUFY_PASSWORD=your-password
```

Then use the library directly:

```python
import asyncio
import os
from dotenv import load_dotenv
from custom_components.robovac_mqtt.EufyClean import EufyClean

load_dotenv()

async def main():
    eufy = EufyClean(os.getenv("EUFY_USERNAME"), os.getenv("EUFY_PASSWORD"))
    await eufy.init()

    devices = await eufy.get_devices()
    device_id = next((d["deviceId"] for d in devices if d), None)
    if not device_id:
        print("No devices found")
        return

    device = await eufy.init_device(device_id)
    await device.connect()

    print("Status:", await device.get_work_status())
    print("Battery:", await device.get_battery_level())

    # await device.go_home()
    # await device.scene_clean(4)

asyncio.run(main())
```

See `standalone_example.py` for a more detailed example with error handling.

## Project Structure

```
eufy-clean/
├── custom_components/
│   └── robovac_mqtt/
│       ├── EufyApi.py          # Eufy cloud API client
│       ├── EufyClean.py        # Main device manager
│       ├── __init__.py         # HA integration setup
│       ├── button.py           # HA button entities
│       ├── config_flow.py      # HA config flow
│       ├── constants/          # Protocol constants
│       ├── controllers/        # Device controllers
│       ├── manifest.json       # HA integration manifest
│       ├── proto/              # Protobuf definitions
│       ├── utils.py            # Utility functions
│       └── vacuum.py           # HA vacuum entity
├── example.py                  # Standalone usage example
├── standalone_example.py       # Detailed standalone example
├── requirements.txt            # Full deps (includes Home Assistant)
├── requirements-standalone.txt # Lightweight standalone deps
├── pyproject.toml
├── docker-compose.yml
└── hacs.json
```

## Roadmap

- [ ] Clean rooms with custom cleaning mode
- [ ] Track consumables (water, dustbin, filter)
- [ ] Error tracking and reporting
- [ ] Map management
- [ ] Device location / current position
- [ ] Support for additional Eufy models

## License

See [LICENSE.md](LICENSE.md).

## Credits

Originally forked from [martijnpoppen/eufy-clean](https://github.com/martijnpoppen/eufy-clean). Rewritten in Python with Home Assistant integration.
