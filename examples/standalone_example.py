#!/usr/bin/env python3
"""
Standalone Example - Use Eufy Clean library without Home Assistant

This demonstrates that you can use the library directly in Python
without needing Home Assistant installed.

Requirements:
    pip install aiohttp paho-mqtt protobuf python-dotenv

Setup:
    1. Create .env file with:
       EUFY_USERNAME=your-email@example.com
       EUFY_PASSWORD=your-password
    2. Run: python standalone_example.py
"""
import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path so we can import
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from dotenv import load_dotenv
    from custom_components.robovac_mqtt.EufyClean import EufyClean
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("\nPlease install dependencies:")
    print("  pip install aiohttp paho-mqtt protobuf python-dotenv")
    sys.exit(1)


async def main():
    """Main function demonstrating standalone usage"""
    
    # Load environment variables
    load_dotenv()
    
    username = os.getenv('EUFY_USERNAME')
    password = os.getenv('EUFY_PASSWORD')
    
    if not username or not password:
        print("❌ Error: EUFY_USERNAME and EUFY_PASSWORD must be set")
        print("\nCreate a .env file with:")
        print("  EUFY_USERNAME=your-email@example.com")
        print("  EUFY_PASSWORD=your-password")
        return
    
    print("=" * 60)
    print("Eufy Clean - Standalone Example")
    print("(No Home Assistant Required!)")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Initialize
        print("🔐 Logging in to Eufy...")
        eufy_clean = EufyClean(username, password)
        await eufy_clean.init()
        print("✅ Login successful!")
        print()
        
        # Step 2: Get devices
        print("📱 Fetching devices...")
        devices = await eufy_clean.get_devices()
        print(f"✅ Found {len(devices)} device(s)")
        print()
        
        if not devices:
            print("⚠️  No devices found. Make sure your device supports MQTT.")
            return
        
        # Step 3: Display device info
        for i, device_info in enumerate(devices, 1):
            print(f"Device {i}:")
            print(f"  Name: {device_info.get('deviceName', 'Unknown')}")
            print(f"  ID: {device_info.get('deviceId', 'Unknown')}")
            print(f"  Model: {device_info.get('deviceModel', 'Unknown')}")
            print()
        
        # Step 4: Connect to first device
        device_info = devices[0]
        print(f"🔌 Connecting to: {device_info['deviceName']}...")
        
        device = await eufy_clean.init_device(device_info['deviceId'])
        await device.connect()
        print("✅ Connected to device!")
        print()
        
        # Wait a moment for initial data
        print("⏳ Waiting for device data...")
        await asyncio.sleep(3)
        print()
        
        # Step 5: Query device information
        print("📊 Device Status:")
        print("-" * 60)
        
        try:
            battery = await device.get_battery_level()
            print(f"  🔋 Battery: {battery}%")
        except Exception as e:
            print(f"  🔋 Battery: Error - {e}")
        
        try:
            status = await device.get_work_status()
            print(f"  📍 Status: {status}")
        except Exception as e:
            print(f"  📍 Status: Error - {e}")
        
        try:
            mode = await device.get_work_mode()
            print(f"  ⚙️  Mode: {mode}")
        except Exception as e:
            print(f"  ⚙️  Mode: Error - {e}")
        
        try:
            speed = await device.get_clean_speed()
            print(f"  🚀 Speed: {speed}")
        except Exception as e:
            print(f"  🚀 Speed: Error - {e}")
        
        print()
        print("=" * 60)
        print("✅ Success! Library works standalone!")
        print("=" * 60)
        print()
        print("You can now use this library in your own Python projects")
        print("without needing Home Assistant!")
        print()
        
        # Example commands (commented out - uncomment to test)
        # print("Example commands you can run:")
        # print("  await device.auto_clean()      # Start cleaning")
        # print("  await device.go_home()         # Return to base")
        # print("  await device.pause()           # Pause cleaning")
        # print("  await device.room_clean([1, 2], map_id=4)  # Clean specific rooms")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    print()
    asyncio.run(main())
