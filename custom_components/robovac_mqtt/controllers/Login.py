"""Authentication controller.

Manages Eufy cloud login, MQTT credential retrieval, and device list
resolution (matching cloud device records with MQTT-connected devices).
"""
from typing import Any

from ..controllers.Base import Base
from ..EufyApi import EufyApi


# TODO: Normalize camelCase method names to snake_case for PEP 8 consistency.
#       Deferred to avoid breaking callers in a single pass — affects:
#       getDevices, getMqttDevice, checkLogin, checkApiType, findModel
class EufyLogin(Base):
    def __init__(self, username: str, password: str, openudid: str):
        super().__init__()
        self.eufyApi = EufyApi(username, password, openudid)
        self.username = username
        self.password = password
        self.sid = None
        self.mqtt_credentials = None
        self.mqtt_devices = []
        self.eufy_api_devices = []

    async def init(self) -> None:
        await self.login({'mqtt': True})
        return await self.getDevices()

    async def login(self, config: dict) -> None:
        eufyLogin = None

        if not config['mqtt']:
            raise Exception('MQTT login is required')

        eufyLogin = await self.eufyApi.login()

        if not eufyLogin:
            raise Exception('Login failed - Please check your username and password. Error: Incorrect email login or password.')

        if not config['mqtt']:
            raise Exception('MQTT login is required')

        if 'mqtt' not in eufyLogin:
            raise Exception('Login succeeded but MQTT credentials not available')

        self.mqtt_credentials = eufyLogin['mqtt']

    async def checkLogin(self) -> None:
        if not self.sid:
            await self.login({'mqtt': True})

    async def getDevices(self) -> None:
        self.eufy_api_devices = await self.eufyApi.get_cloud_device_list()
        devices = await self.eufyApi.get_device_list()
        devices = [
            {
                **self.findModel(device['device_sn']),
                'apiType': self.checkApiType(device.get('dps', {})),
                'mqtt': True,
                'dps': device.get('dps', {})
            }
            for device in devices
        ]
        self.mqtt_devices = [d for d in devices if not d['invalid']]

    async def getMqttDevice(self, deviceId: str) -> list[dict[str, Any]] | dict[str, Any] | None:
        return await self.eufyApi.get_device_list(deviceId)

    def checkApiType(self, dps: dict) -> str:
        """Return 'novel' if DPS keys match the expected map, else 'legacy'."""
        if any(k in dps for k in self.dps_map.values()):
            return 'novel'
        return 'legacy'

    def findModel(self, deviceId: str) -> dict[str, Any]:
        device = next((d for d in self.eufy_api_devices if d['id'] == deviceId), None)

        if device:
            return {
                'deviceId': deviceId,
                'deviceModel': device.get('product', {}).get('product_code', '')[:5] or device.get('device_model', '')[:5],
                'deviceName': device.get('alias_name') or device.get('device_name') or device.get('name'),
                'deviceModelName': device.get('product', {}).get('name'),
                'invalid': False
            }

        return {'deviceId': deviceId, 'deviceModel': '', 'deviceName': '', 'deviceModelName': '', 'invalid': True}
