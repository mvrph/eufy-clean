# In-Depth Assessment: Device Query Capabilities

## Executive Summary

**YES, you can send requests to the device using Python** to retrieve various information. The project already has a solid foundation for device communication via MQTT, but **map IDs and room IDs are not currently being queried** - they need to be implemented.

---

## Current Architecture

### Communication Method
- **Protocol**: MQTT over TLS (port 8883)
- **Authentication**: Certificate-based (PEM certificate + private key)
- **Message Format**: JSON-wrapped protobuf messages
- **Topic Pattern**: 
  - Publish: `cmd/eufy_home/{deviceModel}/{deviceId}/req`
  - Subscribe: `cmd/eufy_home/{deviceModel}/{deviceId}/res`

### Data Flow
1. **Login** → Eufy Cloud API → Get MQTT credentials
2. **Connect** → MQTT broker → Subscribe to device responses
3. **Query/Command** → Send protobuf-encoded commands via MQTT
4. **Receive** → Device responds with data via MQTT → Decoded from protobuf

---

## Currently Available Information

### ✅ **Battery Level** - WORKING
- **DPS Key**: `163` (`BATTERY_LEVEL`)
- **Method**: `await device.get_battery_level()`
- **Returns**: Integer (0-100)
- **Status**: ✅ Fully implemented and working

### ✅ **Work Status** - WORKING
- **DPS Key**: `153` (`WORK_STATUS`)
- **Method**: `await device.get_work_status()`
- **Returns**: String enum (IDLE, CLEANING, DOCKED, RETURNING, ERROR, etc.)
- **Status**: ✅ Fully implemented and working
- **Details**: Decodes `WorkStatus` protobuf message with state information

### ✅ **Work Mode** - WORKING
- **DPS Key**: `153` (`WORK_MODE`)
- **Method**: `await device.get_work_mode()`
- **Returns**: String (auto, select_room, select_zone, spot, fast_mapping, etc.)
- **Status**: ✅ Fully implemented and working

### ✅ **Clean Speed** - WORKING
- **DPS Key**: `158` (`CLEAN_SPEED`)
- **Method**: `await device.get_clean_speed()`
- **Returns**: String (quiet, standard, turbo, max)
- **Status**: ✅ Fully implemented and working

### ✅ **Clean Parameters** - WORKING
- **DPS Key**: `154` (`CLEANING_PARAMETERS`)
- **Method**: `await device.get_clean_params_response()`
- **Returns**: `CleanParamResponse` protobuf object
- **Status**: ✅ Fully implemented and working
- **Contains**: Clean type, extent, mop mode, etc.

### ✅ **Error Codes** - WORKING
- **DPS Key**: `177` (`ERROR_CODE`)
- **Method**: `await device.get_error_code()`
- **Returns**: Error code integer
- **Status**: ✅ Fully implemented and working

### ✅ **Device Status (via DPS)** - WORKING
- **Method**: `await device.get_robovac_data()`
- **Returns**: Dictionary of all mapped DPS values
- **Status**: ✅ Available but not all keys are mapped

---

## Missing Information (Not Currently Implemented)

### ❌ **Map IDs** - NOT IMPLEMENTED
- **Status**: ❌ Not currently queried
- **Available via**: 
  - `UniversalDataResponse` protobuf (contains `cur_map_room.map_id`)
  - `MultiMapsManageRequest` with method `MAP_GET_ALL` or `MAP_GET_ONE`
  - Potentially in `WorkStatus` or other status messages
- **DPS Key**: Unknown - may need to query via protobuf command
- **Recommendation**: Implement query method using `UniversalDataRequest` or map management commands

### ❌ **Room IDs** - NOT IMPLEMENTED
- **Status**: ❌ Not currently queried
- **Available via**: 
  - `UniversalDataResponse.RoomTable` contains room data with IDs and names
  - Structure: `cur_map_room.data[]` with `id`, `name`, and `scene` fields
- **DPS Key**: Unknown - likely needs protobuf query
- **Recommendation**: Implement `get_rooms()` method that queries `UniversalDataRequest`

### ❌ **Room Names** - NOT IMPLEMENTED
- **Status**: ❌ Not currently queried
- **Available via**: `UniversalDataResponse.RoomTable.Data.name`
- **Recommendation**: Part of room ID implementation

### ❌ **Multiple Maps** - NOT IMPLEMENTED
- **Status**: ❌ Not currently queried
- **Available via**: `MultiMapsManageResponse` with `MAP_GET_ALL` method
- **Recommendation**: Implement `get_all_maps()` method

### ❌ **Map Details** - NOT IMPLEMENTED
- **Status**: ❌ Not currently queried
- **Available via**: `MultiMapsManageResponse.CompleteMaps` or `MapInfo` protobuf
- **Contains**: Map ID, name, dimensions, room outlines, restricted zones, etc.
- **Recommendation**: Implement map query methods

---

## Available Data Point Service (DPS) Keys

The project uses Tuya's DPS (Data Point Service) protocol. Currently mapped keys:

```python
dps_map = {
    'PLAY_PAUSE': '152',           # Control commands
    'DIRECTION': '155',            # Direction control
    'WORK_MODE': '153',            # Work mode
    'WORK_STATUS': '153',          # Work status (same as WORK_MODE)
    'CLEANING_PARAMETERS': '154',  # Clean parameters
    'CLEANING_STATISTICS': '167',  # Statistics (not used)
    'ACCESSORIES_STATUS': '168',   # Accessories (not used)
    'GO_HOME': '173',              # Go home command
    'CLEAN_SPEED': '158',          # Clean speed
    'FIND_ROBOT': '160',           # Find robot
    'BATTERY_LEVEL': '163',        # Battery level
    'ERROR_CODE': '177',           # Error codes
}
```

**Note**: There may be additional DPS keys not yet mapped. You can inspect the raw `dps` dictionary from `get_device_list()` to discover more.

---

## How to Query Device Information

### Current Implementation Pattern

```python
# 1. Initialize and connect
eufy_clean = EufyClean(username, password)
await eufy_clean.init()
device = await eufy_clean.init_device(device_id)
await device.connect()

# 2. Query available information
battery = await device.get_battery_level()
status = await device.get_work_status()
mode = await device.get_work_mode()
speed = await device.get_clean_speed()
params = await device.get_clean_params_response()
error = await device.get_error_code()

# 3. Get all raw data
all_data = await device.get_robovac_data()
```

### How Data is Retrieved

1. **Automatic Updates**: When device connects, it subscribes to MQTT topic and receives push updates
2. **Data Mapping**: Incoming DPS data is automatically mapped via `_map_data()` method
3. **Protobuf Decoding**: Binary data is decoded from base64 using protobuf definitions
4. **Cached Data**: Data is stored in `self.robovac_data` dictionary

---

## Recommendations for Adding Map/Room ID Queries

### Option 1: Query Universal Data (Recommended)

The `UniversalDataRequest`/`UniversalDataResponse` protobuf is designed for this:

```python
# Add to SharedConnect class
async def get_rooms_and_map(self):
    """Query current map ID and room information"""
    from ..proto.cloud.universal_data_pb2 import UniversalDataRequest, UniversalDataResponse
    from ..utils import encode, decode
    
    # Create request
    request = UniversalDataRequest()
    request_data = encode_message(request)
    
    # Send via DPS - need to find the correct DPS key
    # Likely a new DPS key like '169' or '170' for universal data
    # This would need to be discovered by:
    # 1. Inspecting device responses
    # 2. Checking Eufy API documentation
    # 3. Reverse engineering the app
    
    # For now, hypothetical implementation:
    response_data = await self.send_command({self.dps_map.get('UNIVERSAL_DATA', '169'): request_data})
    
    # Decode response
    response = decode(UniversalDataResponse, response_data)
    
    return {
        'map_id': response.cur_map_room.map_id,
        'rooms': [
            {
                'id': room.id,
                'name': room.name,
                'scene': room.scene
            }
            for room in response.cur_map_room.data
        ]
    }
```

### Option 2: Query via Map Management

```python
async def get_all_maps(self):
    """Get all available maps"""
    from ..proto.cloud.multi_maps_pb2 import MultiMapsManageRequest, MultiMapsManageResponse
    from ..utils import encode
    
    request = MultiMapsManageRequest(
        method=MultiMapsManageRequest.Method.MAP_GET_ALL,
        seq=1
    )
    
    # Send command - need correct DPS key
    request_data = encode_message(request)
    response = await self.send_command({self.dps_map.get('MAP_MANAGE', '170'): request_data})
    
    # Note: According to proto comments, MAP_GET_ALL uses P2P, not DPS
    # This might require a different communication channel
```

### Option 3: Inspect Existing Device Data

The device list API already returns some DPS data:

```python
# In Login.py, getDevices() already fetches:
devices = await self.eufyApi.get_device_list()
# Each device has a 'dps' dictionary

# You could inspect this:
for device in devices:
    print(f"Device {device['device_sn']} DPS keys: {device.get('dps', {}).keys()}")
    # Look for keys that might contain map/room info
```

---

## Implementation Steps

### Step 1: Discover DPS Keys
1. Add debug logging to see all incoming DPS data
2. Inspect `device.get('dps', {})` from `get_device_list()`
3. Monitor MQTT messages for any map/room related data

### Step 2: Test Universal Data Query
1. Try sending `UniversalDataRequest` via different DPS keys
2. Start with common keys: `169`, `170`, `171`, `172`
3. Monitor responses for `UniversalDataResponse`

### Step 3: Implement Room Query Method
1. Add `get_rooms()` method to `SharedConnect`
2. Handle the response parsing
3. Cache results in `robovac_data`

### Step 4: Implement Map Query Method
1. Add `get_current_map_id()` method
2. Add `get_all_maps()` method (if P2P is available)
3. Handle map selection/switching

---

## Current Limitations

1. **No Active Querying**: The system relies on push updates from device, not active queries
2. **Unknown DPS Keys**: Map/room data DPS keys are not documented
3. **P2P Requirement**: Some map operations may require P2P connection (not MQTT)
4. **Protobuf Complexity**: Need to understand protobuf message structure

---

## What You Can Do Right Now

### ✅ Immediate Actions

1. **Query Battery**: `await device.get_battery_level()`
2. **Query Status**: `await device.get_work_status()`
3. **Query Mode**: `await device.get_work_mode()`
4. **Query Speed**: `await device.get_clean_speed()`
5. **Query Parameters**: `await device.get_clean_params_response()`
6. **Inspect Raw Data**: `await device.get_robovac_data()`
7. **Inspect Device List DPS**: Check `device['dps']` from `get_devices()`

### 🔧 Development Actions

1. **Add Debug Logging**: Enable `debug=True` in device config to see all MQTT messages
2. **Inspect DPS Keys**: Print all keys from `device.get('dps', {})` to find unmapped ones
3. **Monitor MQTT**: Watch the MQTT topic for any map/room related messages
4. **Test Universal Data**: Try sending `UniversalDataRequest` via various DPS keys

---

## Code Examples

### Example: Query All Available Information

```python
import asyncio
import os
from custom_components.robovac_mqtt.EufyClean import EufyClean

async def query_device_info():
    eufy_clean = EufyClean(os.getenv('EUFY_USERNAME'), os.getenv('EUFY_PASSWORD'))
    await eufy_clean.init()
    
    devices = await eufy_clean.get_devices()
    print(f"Found {len(devices)} devices")
    
    for device_info in devices:
        print(f"\n=== Device: {device_info['deviceName']} ===")
        print(f"Device ID: {device_info['deviceId']}")
        print(f"Model: {device_info['deviceModel']}")
        
        # Inspect raw DPS data
        if 'dps' in device_info:
            print(f"\nAvailable DPS Keys: {list(device_info['dps'].keys())}")
            for key, value in device_info['dps'].items():
                print(f"  DPS {key}: {value}")
        
        # Connect and query
        device = await eufy_clean.init_device(device_info['deviceId'])
        await device.connect()
        
        # Query available info
        print(f"\nBattery: {await device.get_battery_level()}%")
        print(f"Status: {await device.get_work_status()}")
        print(f"Mode: {await device.get_work_mode()}")
        print(f"Speed: {await device.get_clean_speed()}")
        
        # Get all data
        all_data = await device.get_robovac_data()
        print(f"\nAll Robovac Data:")
        for key, value in all_data.items():
            print(f"  {key}: {value}")

if __name__ == '__main__':
    asyncio.run(query_device_info())
```

### Example: Discover New DPS Keys

```python
async def discover_dps_keys():
    eufy_clean = EufyClean(username, password)
    await eufy_clean.init()
    devices = await eufy_clean.get_devices()
    
    for device_info in devices:
        if 'dps' in device_info:
            print(f"Device {device_info['deviceId']} DPS keys:")
            for key, value in device_info['dps'].items():
                print(f"  Key {key}: {type(value).__name__} = {value}")
                # Try to decode as protobuf if it looks like base64
                if isinstance(value, str) and len(value) > 20:
                    try:
                        from base64 import b64decode
                        data = b64decode(value)
                        print(f"    Decoded length: {len(data)} bytes")
                    except:
                        pass
```

---

## Conclusion

**You CAN query device information via Python**, and the infrastructure is already in place. The project successfully retrieves:
- ✅ Battery level
- ✅ Work status
- ✅ Work mode
- ✅ Clean speed
- ✅ Clean parameters
- ✅ Error codes

**Map IDs and Room IDs are NOT currently implemented**, but the protobuf definitions exist (`UniversalDataResponse`, `MultiMapsManageResponse`) suggesting this functionality is available - it just needs to be implemented.

**Next Steps**:
1. Enable debug logging to see all MQTT messages
2. Inspect the DPS dictionary from `get_device_list()` to find map/room related keys
3. Implement `get_rooms()` and `get_map_id()` methods using `UniversalDataRequest`
4. Test with your specific device to discover the correct DPS keys

The foundation is solid - you just need to add the map/room query methods!
