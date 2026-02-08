# Eufy Clean

Home Assistant custom integration for controlling Eufy robot vacuums over MQTT. Built for the **Robovac X10 Pro Omni** but should work with other MQTT-enabled Eufy vacuums.

Originally based on [eufy-clean](https://github.com/martijnpoppen/eufy-clean) by [martijnpoppen](https://github.com/martijnpoppen), rewritten in Python with Home Assistant support.

## Features

- Cloud login and device pairing via Eufy API
- Real-time vacuum control over MQTT
- Home Assistant config flow integration
- Scene cleaning and room-specific cleaning
- Battery level sensor (useful for off-peak charging schedules)
- Standalone Python usage without Home Assistant

## Requirements

- Python 3.12+
- An MQTT-enabled Eufy vacuum (e.g. Robovac X10 Pro Omni)
- Home Assistant (optional — can be used standalone)

## Installation

### Home Assistant (HACS)

1. Add this repository to [HACS](https://hacs.xyz/) as a custom integration
2. Install **Eufy Robovac MQTT**
3. Restart Home Assistant
4. Go to **Settings > Devices & Services > Add Integration** and search for "Eufy Robovac MQTT"
5. Log in with your Eufy app credentials

### Standalone

```bash
git clone https://github.com/mvrph/eufy-clean.git
cd eufy-clean
pip install -r requirements.txt
```

## Usage

### Home Assistant Services

**Scene cleaning:**

```yaml
action: vacuum.send_command
data:
  command: scene_clean
  params:
    scene: 5
target:
  entity_id: vacuum.robovac_x10_pro_omni
```

Scene numbers: 1 = full home daily, 2 = full home deep, 3 = post-meal. Custom scenes start at 4, incrementing in the order you created them in the app.

**Room cleaning:**

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

Room IDs are assigned by the mapping order — starting from the room left of the base station and incrementing. The base station room is last. You can verify IDs by testing `vacuum.room_clean` and checking the app.

> [!TIP]
> If you get "Unable to identify position", it's likely because you've had multiple maps and your default `map_id` is higher than expected. Try incrementing — 20 is not an unusual number.

### Standalone Python

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

### Battery Sensor

The integration exposes a battery charge sensor in Home Assistant, useful for tracking charge level and scheduling off-peak charging.

![Battery sensor in Home Assistant](assets/eufy-battery.png)

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
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
└── hacs.json
```

## TODO

- [ ] Clean rooms with custom cleaning mode
- [ ] Track consumables (water, dustbin, filter)
- [ ] Error tracking and reporting
- [ ] Map management
- [ ] Device location / current position
- [ ] Support for additional Eufy models

## License

See [LICENSE.md](LICENSE.md).

## Credits

Forked from [martijnpoppen/eufy-clean](https://github.com/martijnpoppen/eufy-clean). Rewritten in Python with Home Assistant integration.
