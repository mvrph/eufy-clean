# Eufy Clean - Robovac MQTT Controller

## Overview
A Python library and Home Assistant custom integration for controlling Eufy robot vacuums over MQTT. Built for the Robovac X10 Pro Omni but works with other MQTT-enabled Eufy vacuums.

In this Replit environment, it runs in **standalone mode** (without Home Assistant).

## Current State
- Project is set up with Python 3.12 and Poetry for dependency management
- The `homeassistant` dependency has been removed from pyproject.toml since it's not compatible with this environment; only standalone dependencies are installed
- The standalone example (`standalone_example.py`) runs and requires `EUFY_USERNAME` and `EUFY_PASSWORD` environment variables to connect to a real device

## Project Architecture

### Key Files
- `standalone_example.py` — Main entry point for standalone usage
- `example.py` — Alternative standalone example
- `custom_components/robovac_mqtt/` — Core library code
  - `EufyApi.py` — Eufy cloud API client
  - `EufyClean.py` — Main device manager
  - `controllers/` — Device controllers
  - `proto/` — Protobuf definitions
  - `constants/` — Protocol constants
  - `utils.py` — Utility functions
- `pyproject.toml` — Poetry configuration (standalone deps only)
- `requirements-standalone.txt` — Minimal standalone requirements

### How It Works
1. Authenticates with Eufy cloud API using email/password
2. Discovers MQTT-enabled vacuum devices
3. Connects to devices via MQTT for real-time control
4. Supports commands: clean, pause, go home, room clean, scene clean, etc.

## Running
Set environment variables `EUFY_USERNAME` and `EUFY_PASSWORD`, then run `standalone_example.py`.

## Recent Changes
- 2026-02-10: Initial Replit setup. Removed `homeassistant` dependency, added `aiohttp` for standalone usage. Configured workflow to run standalone example.
