from homeassistant.helpers.entity_platform import EntityPlatform
from .sensor import setup_platform

def setup(hass, config):
    """Set up the Bognor Data component."""
    # Fetch the data
    hass.helpers.discovery.load_platform('sensor', 'bognor_data', {}, config)

    return True