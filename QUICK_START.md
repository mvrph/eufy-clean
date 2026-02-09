# Quick Start - Standalone Usage

## ✅ All You Need: Username & Password

That's it! Just your Eufy account credentials.

---

## Step 1: Install Dependencies

Run this command:

```bash
pip install aiohttp paho-mqtt protobuf python-dotenv
```

Or use the setup script:
```bash
./setup_standalone.sh
```

---

## Step 2: Set Your Credentials

Create a `.env` file in this directory:

```bash
EUFY_USERNAME=your-email@example.com
EUFY_PASSWORD=your-password
```

**That's all you need!** No MQTT broker, no Home Assistant, no special setup.

---

## Step 3: Verify Everything is Ready

Run the verification script:

```bash
python3 ready_to_use.py
```

This will check:
- ✅ Dependencies are installed
- ✅ Credentials are set
- ✅ Library can be imported

---

## Step 4: Use It!

Run the example:
```bash
python3 standalone_example.py
```

Or use in your own code:
```python
import asyncio
from custom_components.robovac_mqtt.EufyClean import EufyClean

async def main():
    eufy_clean = EufyClean("your-email", "your-password")
    await eufy_clean.init()
    
    device = await eufy_clean.init_device(device_id)
    await device.connect()
    
    battery = await device.get_battery_level()
    print(f"Battery: {battery}%")

asyncio.run(main())
```

---

## What Happens Behind the Scenes

1. **Login** → Connects to Eufy API with your credentials
2. **Get MQTT Credentials** → Automatically retrieves MQTT broker info
3. **Connect to Device** → Connects to Eufy's MQTT broker (no setup needed!)
4. **Query/Control** → Send commands and get device status

**Everything is automatic** - you just provide username and password!

---

## Troubleshooting

**"Module not found" errors?**
```bash
pip install aiohttp paho-mqtt protobuf python-dotenv
```

**"Credentials not found"?**
Create `.env` file with your Eufy email and password.

**"Connection failed"?**
- Check your internet connection
- Verify credentials are correct
- Make sure your device supports MQTT (Robovac X10 Pro Omni, etc.)

---

## Summary

✅ **4 dependencies** (aiohttp, paho-mqtt, protobuf, python-dotenv)  
✅ **2 credentials** (username, password)  
✅ **0 additional setup** (no MQTT broker, no Home Assistant)

**That's it!** 🎉
