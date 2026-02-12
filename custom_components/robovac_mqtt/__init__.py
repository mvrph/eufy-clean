import logging

# Home Assistant imports - only needed for HA integration
try:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.const import Platform
    from homeassistant.core import HomeAssistant
    from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
    try:
        from .constants.hass import DOMAIN, VACS, DEVICES
    except ImportError:
        # Fallback if constants not available
        DOMAIN = "robovac_mqtt"
        VACS = "vacs"
        DEVICES = "devices"
    
    PLATFORMS = [Platform.VACUUM, Platform.BUTTON]
    _LOGGER = logging.getLogger(__name__)
    
    # Home Assistant integration functions
    async def async_setup(hass: HomeAssistant, _) -> bool:
        hass.data.setdefault(DOMAIN, {VACS: {}, DEVICES: {}})
        return True
    
    async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
        entry.async_on_unload(entry.add_update_listener(update_listener))
    
        # Init EufyClean
        username = entry.data[CONF_USERNAME]
        password = entry.data[CONF_PASSWORD]
        eufy_clean = EufyClean(username, password)
        await eufy_clean.init()
    
        # Load devices
        for vacuum in await eufy_clean.get_devices():
            device = await eufy_clean.init_device(vacuum['deviceId'])
            await device.connect()
            _LOGGER.info("Adding %s", device.device_id)
            hass.data[DOMAIN][DEVICES][device.device_id] = device
    
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
        return True
    
    async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
        await hass.config_entries.async_reload(entry.entry_id)

except ImportError:
    _LOGGER = logging.getLogger(__name__)

# Core library imports - always available
from .EufyClean import EufyClean
