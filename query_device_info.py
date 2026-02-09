#!/usr/bin/env python3
"""
Example script to query device information and discover map/room IDs.

This script demonstrates:
1. How to connect to a Eufy device
2. How to query available device information
3. How to inspect DPS keys for map/room data
4. How to attempt to query universal data (map/room info)
"""

import asyncio
import os
import json
from base64 import b64decode, b64encode

from custom_components.robovac_mqtt.EufyClean import EufyClean
from custom_components.robovac_mqtt.proto.cloud.universal_data_pb2 import (
    UniversalDataRequest,
    UniversalDataResponse
)
from custom_components.robovac_mqtt.utils import encode_message, decode


async def query_device_info():
    """Query all available device information"""
    
    # Initialize
    username = os.getenv('EUFY_USERNAME')
    password = os.getenv('EUFY_PASSWORD')
    
    if not username or not password:
        print("Error: Please set EUFY_USERNAME and EUFY_PASSWORD environment variables")
        return
    
    print("=" * 60)
    print("Eufy Device Information Query Tool")
    print("=" * 60)
    
    eufy_clean = EufyClean(username, password)
    await eufy_clean.init()
    
    devices = await eufy_clean.get_devices()
    print(f"\nFound {len(devices)} device(s)\n")
    
    for device_info in devices:
        print(f"{'=' * 60}")
        print(f"Device: {device_info.get('deviceName', 'Unknown')}")
        print(f"Device ID: {device_info.get('deviceId', 'Unknown')}")
        print(f"Model: {device_info.get('deviceModel', 'Unknown')}")
        print(f"Model Name: {device_info.get('deviceModelName', 'Unknown')}")
        print(f"{'=' * 60}\n")
        
        # Inspect raw DPS data from device list
        if 'dps' in device_info and device_info['dps']:
            print("📊 Raw DPS Data from Device List:")
            print("-" * 60)
            for key, value in device_info['dps'].items():
                value_str = str(value)
                if len(value_str) > 100:
                    value_str = value_str[:100] + "..."
                print(f"  DPS Key {key}: {value_str}")
                print(f"    Type: {type(value).__name__}")
                
                # Try to decode if it looks like base64
                if isinstance(value, str) and len(value) > 20:
                    try:
                        decoded = b64decode(value)
                        print(f"    Decoded: {len(decoded)} bytes")
                        if len(decoded) > 0:
                            print(f"    First bytes: {decoded[:20].hex()}")
                    except Exception as e:
                        pass
            print()
        
        # Connect to device
        print("🔌 Connecting to device...")
        try:
            device = await eufy_clean.init_device(device_info['deviceId'])
            await device.connect()
            print("✅ Connected successfully\n")
            
            # Wait a bit for initial data
            await asyncio.sleep(2)
            
            # Query available information
            print("📈 Querying Device Status:")
            print("-" * 60)
            
            try:
                battery = await device.get_battery_level()
                print(f"  Battery Level: {battery}%")
            except Exception as e:
                print(f"  Battery Level: Error - {e}")
            
            try:
                status = await device.get_work_status()
                print(f"  Work Status: {status}")
            except Exception as e:
                print(f"  Work Status: Error - {e}")
            
            try:
                mode = await device.get_work_mode()
                print(f"  Work Mode: {mode}")
            except Exception as e:
                print(f"  Work Mode: Error - {e}")
            
            try:
                speed = await device.get_clean_speed()
                print(f"  Clean Speed: {speed}")
            except Exception as e:
                print(f"  Clean Speed: Error - {e}")
            
            try:
                error = await device.get_error_code()
                print(f"  Error Code: {error}")
            except Exception as e:
                print(f"  Error Code: Error - {e}")
            
            try:
                params = await device.get_clean_params_response()
                if params:
                    print(f"  Clean Parameters: {params}")
            except Exception as e:
                print(f"  Clean Parameters: Error - {e}")
            
            print()
            
            # Get all mapped data
            print("🗂️  All Mapped Robovac Data:")
            print("-" * 60)
            try:
                all_data = await device.get_robovac_data()
                if all_data:
                    for key, value in all_data.items():
                        value_str = str(value)
                        if len(value_str) > 200:
                            value_str = value_str[:200] + "..."
                        print(f"  {key}: {value_str}")
                else:
                    print("  No data available")
            except Exception as e:
                print(f"  Error: {e}")
            
            print()
            
            # Attempt to query universal data (map/room info)
            print("🗺️  Attempting to Query Map/Room Information:")
            print("-" * 60)
            await attempt_universal_data_query(device)
            
            print()
            
        except Exception as e:
            print(f"❌ Error connecting to device: {e}")
            import traceback
            traceback.print_exc()
            print()


async def attempt_universal_data_query(device):
    """Attempt to query universal data (map/room info) via different DPS keys"""
    
    # Known DPS keys to try (common ones that might contain map/room data)
    potential_dps_keys = ['169', '170', '171', '172', '174', '175', '176']
    
    # Create UniversalDataRequest
    request = UniversalDataRequest()
    
    try:
        request_data = encode_message(request)
        print(f"  Created UniversalDataRequest: {len(request_data)} chars")
    except Exception as e:
        print(f"  Error creating request: {e}")
        return
    
    # Try to get current DPS data to see what keys are available
    try:
        current_data = await device.get_robovac_data()
        print(f"  Current DPS keys in robovac_data: {list(current_data.keys())}")
    except:
        pass
    
    # Note: We can't directly query via send_command without knowing the DPS key
    # This is a discovery process - you would need to:
    # 1. Monitor MQTT messages when the app queries map/room data
    # 2. Check device documentation
    # 3. Inspect the app's network traffic
    
    print("  ⚠️  To query map/room data, you need to:")
    print("     1. Find the correct DPS key (likely 169-176 range)")
    print("     2. Send UniversalDataRequest via that DPS key")
    print("     3. Decode the UniversalDataResponse")
    print()
    print("  💡 Try enabling debug mode and monitoring MQTT messages")
    print("     when using the Eufy app to see what DPS keys are used")


async def discover_dps_keys():
    """Helper function to discover all DPS keys from device list"""
    print("\n" + "=" * 60)
    print("DPS Key Discovery")
    print("=" * 60)
    
    username = os.getenv('EUFY_USERNAME')
    password = os.getenv('EUFY_PASSWORD')
    
    if not username or not password:
        print("Error: Please set EUFY_USERNAME and EUFY_PASSWORD")
        return
    
    eufy_clean = EufyClean(username, password)
    await eufy_clean.init()
    devices = await eufy_clean.get_devices()
    
    all_dps_keys = set()
    
    for device_info in devices:
        if 'dps' in device_info:
            keys = device_info['dps'].keys()
            all_dps_keys.update(keys)
            print(f"\nDevice {device_info.get('deviceId', 'Unknown')}:")
            print(f"  DPS Keys: {sorted(keys)}")
    
    print(f"\n📋 All Unique DPS Keys Found: {sorted(all_dps_keys)}")
    print(f"\n💡 Mapped DPS Keys in code:")
    print("   - 152: PLAY_PAUSE")
    print("   - 153: WORK_MODE/WORK_STATUS")
    print("   - 154: CLEANING_PARAMETERS")
    print("   - 155: DIRECTION")
    print("   - 158: CLEAN_SPEED")
    print("   - 160: FIND_ROBOT")
    print("   - 163: BATTERY_LEVEL")
    print("   - 167: CLEANING_STATISTICS")
    print("   - 168: ACCESSORIES_STATUS")
    print("   - 173: GO_HOME")
    print("   - 177: ERROR_CODE")
    print(f"\n🔍 Unmapped DPS Keys: {sorted(set(all_dps_keys) - {'152', '153', '154', '155', '158', '160', '163', '167', '168', '173', '177'})}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--discover':
        asyncio.run(discover_dps_keys())
    else:
        asyncio.run(query_device_info())
