from homeassistant.helpers.entity import EntityPlatform
from .sensor import HighTideSensor, LowTideSensor, TidePercentageSensor, SunriseSensor, SunsetSensor
from .get_data import get_tide_data, filter_tide_data

def setup(hass, config):
    """Set up the Bognor Data component."""
    # Fetch the data
    tide_data = get_tide_data()
    filtered_data = filter_tide_data(tide_data)

    # Create the sensors
    high_tide_sensor = HighTideSensor(filtered_data)
    low_tide_sensor = LowTideSensor(filtered_data)
    tide_percentage_sensor = TidePercentageSensor(filtered_data)
    sunrise_sensor = SunriseSensor(filtered_data)
    sunset_sensor = SunsetSensor(filtered_data)

    # Add the sensors to Home Assistant
    platform = EntityPlatform(hass, "sensor", "bognor_data")
    platform.add_entities([
        high_tide_sensor,
        low_tide_sensor,
        tide_percentage_sensor,
        sunrise_sensor,
        sunset_sensor
    ])

    return True