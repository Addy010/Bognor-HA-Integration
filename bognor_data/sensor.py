from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta
from .get_data import async_get_tide_data, get_tide_data, filter_tide_data


# SENSOR_ID = "bognor_tide_sensor"

class HighTideSensor(Entity):
    def __init__(self, data):
        self._state = None
        self._data = data

    @property
    def name(self):
        return "Next High Tide"

    @property
    def unique_id(self):
        return "next_high_tide"

    @property
    def state(self):
        return self._state

    def update(self):
        self._state = self._data["next_high_tide"]

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_track_time_interval(
                self.hass, self.async_update, timedelta(minutes=5)
            )
        )

    async def async_update(self, time):
        tide_data = await async_get_tide_data(self.hass)
        filtered_data = filter_tide_data(tide_data)
        self._state = filtered_data["next_high_tide"]


class LowTideSensor(Entity):
    def __init__(self, data):
        self._state = None
        self._data = data

    @property
    def name(self):
        return "Next Low Tide"

    @property
    def unique_id(self):
        return "next_low_tide"

    @property
    def state(self):
        return self._state

    def update(self):
        self._state = self._data["next_low_tide"]

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_track_time_interval(
                self.hass, self.async_update, timedelta(minutes=5)
            )
        )

    async def async_update(self, time):
        tide_data = await async_get_tide_data(self.hass)
        filtered_data = filter_tide_data(tide_data)
        self._state = filtered_data["next_low_tide"]


class TidePercentageSensor(Entity):
    def __init__(self, data):
        self._state = None
        self._data = data

    @property
    def name(self):
        return "Current Tide Percentage"

    @property
    def unique_id(self):
        return "current_tide_percentage"

    @property
    def state(self):
        return self._state

    def update(self):
        self._state = self._data["current_tide_percentage"]

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_track_time_interval(
                self.hass, self.async_update, timedelta(minutes=5)
            )
        )

    async def async_update(self, time):
        tide_data = await async_get_tide_data(self.hass)
        filtered_data = filter_tide_data(tide_data)
        self._state = filtered_data["current_tide_percentage"]


class SunriseSensor(Entity):
    def __init__(self, data):
        self._state = None
        self._data = data

    @property
    def name(self):
        return "Sunrise"

    @property
    def unique_id(self):
        return "sunrise"

    @property
    def state(self):
        return self._state

    def update(self):
        self._state = self._data["sunrise"]

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_track_time_interval(
                self.hass, self.async_update, timedelta(minutes=5)
            )
        )

    async def async_update(self, time):
        tide_data = await async_get_tide_data(self.hass)
        filtered_data = filter_tide_data(tide_data)
        self._state = filtered_data["sunrise"]

class SunsetSensor(Entity):
    def __init__(self, data):
        self._state = None
        self._data = data

    @property
    def name(self):
        return "Sunset"

    @property
    def unique_id(self):
        return "sunset"

    @property
    def state(self):
        return self._state

    def update(self):
        self._state = self._data["sunset"]

    async def async_added_to_hass(self):
        self.async_on_remove(
            async_track_time_interval(
                self.hass, self.async_update, timedelta(minutes=5)
            )
        )

    async def async_update(self, time):
        tide_data = await async_get_tide_data(self.hass)
        filtered_data = filter_tide_data(tide_data)
        self._state = filtered_data["sunset"]

async def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    # Fetch the data
    tide_data = await async_get_tide_data(hass)
    filtered_data = filter_tide_data(tide_data)

    # Create the sensors
    high_tide_sensor = HighTideSensor(filtered_data)
    low_tide_sensor = LowTideSensor(filtered_data)
    tide_percentage_sensor = TidePercentageSensor(filtered_data)
    sunrise_sensor = SunriseSensor(filtered_data)
    sunset_sensor = SunsetSensor(filtered_data)

    # Add the sensors to Home Assistant
    add_entities([
        high_tide_sensor,
        low_tide_sensor,
        tide_percentage_sensor,
        sunrise_sensor,
        sunset_sensor
    ])