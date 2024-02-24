from homeassistant.helpers.entity_platform import EntityPlatform
from .sensor import setup_platform
import logging

logger = logging.getLogger(__name__)

def setup(hass, config):
    """Set up the Bognor Data component."""
    # Fetch the data
    logger.error("TEST RUNNING")
    hass.helpers.discovery.load_platform('sensor', 'bognor_data', {}, config)

    return True