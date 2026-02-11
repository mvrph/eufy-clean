# Standalone Usage Guide (Without Home Assistant)

## ✅ Yes, You Can Use This Library Standalone!

The core device communication code **does NOT require Home Assistant**. The library is designed to work both:
- ✅ **Standalone** - Direct Python usage (as shown in `examples/example.py`)
- ✅ **Home Assistant Integration** - Via the custom component

---

## Architecture Overview

```
┌─────────────────────────────────────┐
│   Home Assistant Integration        │  ← Optional (only if using HA)
│   (__init__.py, vacuum.py)          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Core Library (Standalone)         │  ← Works independently!
│   - EufyClean                       │
│   - EufyApi                         │
│   - MqttConnect                     │
│   - SharedConnect                   │
└─────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Dependencies                      │
│   - aiohttp (HTTP requests)         │
│   - paho-mqtt (MQTT client)        │
│   - protobuf (message encoding)     │
└─────────────────────────────────────┘
```

**Key Point**: The core classes (`EufyClean`, `EufyApi`, `MqttConnect`) only use standard Python libraries and **do NOT import Home Assistant**.

---

## Setup for Standalone Usage

### Step 1: Install Minimal Dependencies

Create a `requirements-standalone.txt` with only the core dependencies:

```bash
# Core dependencies only (no Home Assistant)
aiohttp>=3.11.0
paho-mqtt>=2.1.0
protobuf>=5.29.0
python-dotenv>=1.0.0
```

Install them:
```bash
pip install -r requirements-standalone.txt
```

### Step 2: Set Up Environment Variables

Create a `.env` file:
```bash
EUFY_USERNAME=your-email@example.com
EUFY_PASSWORD=your-password
```

### Step 3: Use the Library

```python
import asyncio
import os
from custom_components.robovac_mqtt.EufyClean import EufyClean

async def main():
    # Initialize (no Home Assistant needed!)
    eufy_clean = EufyClean(
        os.getenv('EUFY_USERNAME'), 
        os.getenv('EUFY_PASSWORD')
    )
    
    # Connect
    await eufy_clean.init()
    devices = await eufy_clean.get_devices()
    
    # Get device
    device = await eufy_clean.init_device(devices[0]['deviceId'])
    await device.connect()
    
    # Query information
    battery = await device.get_battery_level()
    status = await device.get_work_status()
    
    print(f"Battery: {battery}%")
    print(f"Status: {status}")

if __name__ == '__main__':
    asyncio.run(main())
```

---

## What You DON'T Need

### ❌ No MQTT Broker Setup Required
- The library connects **directly to Eufy's MQTT broker**
- MQTT credentials are obtained automatically via the Eufy API
- You don't need to set up your own MQTT broker

### ❌ No Home Assistant Installation
- The core library works completely independently
- Home Assistant is only needed if you want to use it as a Home Assistant integration

### ❌ No Special Network Configuration
- Works over standard internet connection
- Uses Eufy's cloud services (same as the official app)

---

## How It Works

### 1. Authentication Flow
```
Your Code
    ↓
EufyClean.login()
    ↓
EufyApi.eufy_login() → Eufy Cloud API
    ↓
Get access_token + MQTT credentials
    ↓
Connect to Eufy's MQTT Broker (endpoint_addr:8883)
```

### 2. Device Communication
```
Your Code
    ↓
device.send_command()
    ↓
MQTT Publish → cmd/eufy_home/{model}/{id}/req
    ↓
Device responds via MQTT → cmd/eufy_home/{model}/{id}/res
    ↓
Your Code receives response
```

**All communication happens via Eufy's infrastructure** - no local setup needed!

---

## Complete Standalone Example

```python
#!/usr/bin/env python3
"""
Standalone example - no Home Assistant required
"""
import asyncio
import os
from dotenv import load_dotenv
from custom_components.robovac_mqtt.EufyClean import EufyClean

async def main():
    # Load environment variables
    load_dotenv()
    
    username = os.getenv('EUFY_USERNAME')
    password = os.getenv('EUFY_PASSWORD')
    
    if not username or not password:
        print("Error: Set EUFY_USERNAME and EUFY_PASSWORD in .env file")
        return
    
    # Initialize (standalone - no HA!)
    print("Initializing EufyClean...")
    eufy_clean = EufyClean(username, password)
    await eufy_clean.init()
    
    # Get devices
    print("Fetching devices...")
    devices = await eufy_clean.get_devices()
    print(f"Found {len(devices)} device(s)")
    
    if not devices:
        print("No devices found!")
        return
    
    # Connect to first device
    device_info = devices[0]
    print(f"\nConnecting to: {device_info['deviceName']}")
    
    device = await eufy_clean.init_device(device_info['deviceId'])
    await device.connect()
    
    # Wait for initial data
    await asyncio.sleep(2)
    
    # Query device information
    print("\n=== Device Information ===")
    battery = await device.get_battery_level()
    status = await device.get_work_status()
    mode = await device.get_work_mode()
    speed = await device.get_clean_speed()
    
    print(f"Battery: {battery}%")
    print(f"Status: {status}")
    print(f"Mode: {mode}")
    print(f"Speed: {speed}")
    
    # You can also send commands
    # await device.auto_clean()
    # await device.go_home()
    # await device.room_clean([1, 2, 3], map_id=4)

if __name__ == '__main__':
    asyncio.run(main())
```

---

## Dependencies Breakdown

### Core Dependencies (Required)
- **aiohttp**: HTTP requests to Eufy API
- **paho-mqtt**: MQTT client for device communication
- **protobuf**: Message encoding/decoding
- **python-dotenv**: Environment variable management (optional, but recommended)

### Home Assistant Dependencies (NOT Required for Standalone)
- `homeassistant` - Only needed if using as HA integration
- `home-assistant-bluetooth` - Only for HA
- All other HA-specific packages - Only for HA

---

## File Structure

```
eufy-clean/
├── custom_components/robovac_mqtt/
│   ├── __init__.py              ← HA integration (optional)
│   ├── vacuum.py                 ← HA integration (optional)
│   ├── config_flow.py            ← HA integration (optional)
│   ├── EufyClean.py              ← ✅ Core (standalone)
│   ├── EufyApi.py                ← ✅ Core (standalone)
│   ├── controllers/
│   │   ├── MqttConnect.py        ← ✅ Core (standalone)
│   │   ├── SharedConnect.py      ← ✅ Core (standalone)
│   │   └── Login.py              ← ✅ Core (standalone)
│   └── proto/                    ← ✅ Core (standalone)
├── examples/
│   ├── standalone_example.py      ← ✅ Full standalone example
│   ├── example.py                 ← ✅ Minimal example
│   ├── query_device_info.py       ← ✅ DPS key discovery
│   └── ready_to_use.py            ← ✅ Dependency checker
├── requirements-standalone.txt   ← Lightweight standalone deps
└── requirements.txt              ← Includes HA (for HA users)
```

**Files marked ✅ work standalone without Home Assistant**

---

## Troubleshooting

### Issue: Import Errors
**Problem**: `ModuleNotFoundError: No module named 'homeassistant'`

**Solution**: You're importing from the wrong file. Use:
```python
# ✅ Correct (standalone)
from custom_components.robovac_mqtt.EufyClean import EufyClean

# ❌ Wrong (HA integration)
from custom_components.robovac_mqtt.vacuum import RoboVacMQTTEntity
```

### Issue: Missing Dependencies
**Problem**: `ModuleNotFoundError: No module named 'aiohttp'`

**Solution**: Install core dependencies:
```bash
pip install aiohttp paho-mqtt protobuf python-dotenv
```

### Issue: Connection Timeout
**Problem**: Can't connect to MQTT broker

**Solution**: 
- Check internet connection
- Verify credentials are correct
- Ensure device supports MQTT (Robovac X10 Pro Omni and similar)

---

## Summary

✅ **YES, you can use this library standalone!**

- ✅ No Home Assistant required
- ✅ No MQTT broker setup needed (uses Eufy's broker)
- ✅ No special network configuration
- ✅ Just install core dependencies and use `EufyClean` class
- ✅ Works exactly like `examples/example.py` shows

The library connects directly to Eufy's cloud services and MQTT broker, just like the official app does. You only need:
1. Python 3.12+
2. Core dependencies (aiohttp, paho-mqtt, protobuf)
3. Your Eufy credentials

That's it! 🎉
