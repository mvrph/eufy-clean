# Eufy RoboVac MQTT Integration

## Overview
A Home Assistant custom component and standalone Python library for controlling Eufy RoboVac devices via MQTT. Supports vacuum control (start, pause, stop, return home), fan speed settings, room/scene cleaning, and station commands (dry mop, wash mop, empty dust bin).

## Project Architecture
```
custom_components/robovac_mqtt/
├── __init__.py              # HA integration entry point (also supports standalone)
├── vacuum.py                # HA vacuum entity
├── button.py                # HA button entities (dry mop, wash mop, dust bin)
├── config_flow.py           # HA config flow for setup
├── EufyApi.py               # Eufy cloud API client
├── EufyClean.py             # High-level device manager
├── utils.py                 # Protobuf encode/decode utilities
├── constants/
│   ├── devices.py           # Device model registry
│   ├── hass.py              # HA domain constants
│   └── state.py             # Enums for states, speeds, controls
├── controllers/
│   ├── Base.py              # DPS key mapping base class
│   ├── Login.py             # Login + device discovery
│   ├── MqttConnect.py       # MQTT connection management
│   └── SharedConnect.py     # Shared device control methods
└── proto/cloud/             # Protobuf definitions and generated code
```

Root-level scripts:
- `standalone_example.py` - Standalone usage example
- `query_device_info.py` - Device info discovery tool
- `ready_to_use.py` - Dependency/setup verification

## Key Dependencies
- aiohttp, paho-mqtt, protobuf, python-dotenv

## Recent Changes
- 2026-02-12: Code cleanup - removed unused imports, dead code, replaced print() with logging, fixed .gitignore duplicates

## Notes
- This is a library/integration project, not a web application. No dev server needed.
- Proto files in `proto/cloud/` are auto-generated; do not manually edit `*_pb2.py` files.
