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

See [`examples/standalone_example.py`](examples/standalone_example.py) for a more detailed example with error handling, and [`docs/standalone-usage.md`](docs/standalone-usage.md) for the full standalone guide.

## Project Structure

```
eufy-clean/
├── custom_components/
│   └── robovac_mqtt/               # HA integration + core library
│       ├── __init__.py             # HA platform setup (standalone-safe)
│       ├── EufyClean.py            # High-level device manager (entry point)
│       ├── EufyApi.py              # Eufy cloud REST API client
│       ├── vacuum.py               # HA vacuum entity
│       ├── button.py               # HA button entities (dry mop, wash, dust)
│       ├── config_flow.py          # HA config flow (login UI)
│       ├── utils.py                # Protobuf encode/decode helpers
│       ├── manifest.json           # HA integration manifest
│       ├── constants/              # Enums, device registry, HA constants
│       │   ├── devices.py          #   Model codes → names, series groups
│       │   ├── state.py            #   Work status, speed, control enums
│       │   └── hass.py             #   DOMAIN, data keys
│       ├── controllers/            # Device communication layer
│       │   ├── Base.py             #   DPS key mapping
│       │   ├── Login.py            #   Cloud auth + device discovery
│       │   ├── MqttConnect.py      #   MQTT transport (TLS, pub/sub)
│       │   └── SharedConnect.py    #   Commands: clean, pause, status, etc.
│       └── proto/cloud/            # Protobuf definitions (.proto + _pb2.py)
├── examples/                       # Standalone usage examples
│   ├── standalone_example.py       #   Full example with error handling
│   ├── example.py                  #   Minimal usage example
│   ├── query_device_info.py        #   DPS key discovery tool
│   └── ready_to_use.py             #   Dependency/credential checker
├── scripts/                        # Setup and helper shell scripts
├── docs/                           # Extended documentation
│   ├── standalone-usage.md         #   Standalone library guide
│   └── device-query-protocol.md    #   DPS keys, MQTT topics, protobuf details
├── requirements.txt                # Full deps (includes Home Assistant)
├── requirements-standalone.txt     # Lightweight standalone deps
├── pyproject.toml                  # Poetry project config
├── docker-compose.yml              # HA dev environment
├── hacs.json                       # HACS metadata
└── LICENSE.md
```

### Architecture overview

```
┌────────────────────────────────────┐
│  Home Assistant Integration        │  ← Optional (vacuum.py, button.py, config_flow.py)
│  (__init__.py registers platforms) │
└──────────────┬─────────────────────┘
               │
               ▼
┌────────────────────────────────────┐
│  Core Library (standalone)         │  ← Works without HA
│  EufyClean → Login → EufyApi      │     (cloud auth, device discovery)
│           → MqttConnect            │     (MQTT transport)
│           → SharedConnect          │     (device commands & queries)
└──────────────┬─────────────────────┘
               │
               ▼
┌────────────────────────────────────┐
│  Protocol Layer                    │
│  proto/cloud/*.proto  →  _pb2.py  │     (protobuf messages)
│  constants/state.py               │     (DPS enums, error codes)
│  utils.py                         │     (encode/decode helpers)
└────────────────────────────────────┘
```

### Key concepts

- **DPS (Data Point Service)**: Tuya-based protocol mapping data to numbered keys (e.g. `163` = battery level). See `controllers/Base.py` for the full map.
- **MQTT topics**: Commands go to `cmd/eufy_home/{model}/{id}/req`, responses arrive on `cmd/eufy_home/{model}/{id}/res`. See `controllers/MqttConnect.py`.
- **Protobuf**: Commands and responses are protobuf-encoded, base64-wrapped, and sent as JSON payloads. Definitions live in `proto/cloud/`.

For a deep dive into the protocol and data points, see [`docs/device-query-protocol.md`](docs/device-query-protocol.md).

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
