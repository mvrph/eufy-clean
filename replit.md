# Eufy Clean - Robovac MQTT Controller

## Overview
A Python library and Home Assistant custom integration for controlling Eufy robot vacuums over MQTT. Built for the Robovac X10 Pro Omni but works with other MQTT-enabled Eufy vacuums.

In this Replit environment, it runs in **standalone mode** (without Home Assistant).

## Current State
- Project is set up with Python 3.12 and Poetry for dependency management
- The `homeassistant` dependency has been removed from pyproject.toml since it's not compatible with this environment; only standalone dependencies are installed
- The standalone example (`examples/standalone_example.py`) runs and requires `EUFY_USERNAME` and `EUFY_PASSWORD` environment variables to connect to a real device

## Project Architecture

### Key Directories
- `custom_components/robovac_mqtt/` — Core library and HA integration code
  - `EufyClean.py` — High-level entry point
  - `EufyApi.py` — Eufy cloud REST API client
  - `controllers/` — Auth (Login), MQTT transport (MqttConnect), device commands (SharedConnect)
  - `constants/` — Device registry, state enums, HA constants
  - `proto/cloud/` — Protobuf definitions for device protocol
  - `utils.py` — Protobuf encode/decode helpers
- `examples/` — Standalone usage examples and tools
- `scripts/` — Setup helper shell scripts
- `docs/` — Extended documentation (standalone guide, protocol reference)

### How It Works
1. Authenticates with Eufy cloud API using email/password
2. Discovers MQTT-enabled vacuum devices
3. Connects to devices via MQTT (TLS, port 8883) for real-time control
4. Supports commands: clean, pause, go home, room clean, scene clean, etc.

## Running
Set environment variables `EUFY_USERNAME` and `EUFY_PASSWORD`, then run `examples/standalone_example.py`.

## Recent Changes
- 2026-02-10: Reorganized repo layout — moved docs into `docs/`, scripts into `scripts/`, examples into `examples/`. Added module docstrings and `__init__.py` files. Removed duplicate requirements. Updated README with architecture overview.
- 2026-02-10: Initial Replit setup. Removed `homeassistant` dependency, added `aiohttp` for standalone usage.
