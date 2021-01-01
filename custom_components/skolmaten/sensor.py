from bs4 import BeautifulSoup
from datetime import timedelta,datetime
import requests, json, sys

import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity, generate_entity_id

from homeassistant.components.sensor import PLATFORM_SCHEMA, ENTITY_ID_FORMAT
from homeassistant.const import (CONF_NAME)

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME       = 'Skolmaten'
CONF_SENSORS       = 'sensors'

SENSOR_OPTIONS = {
    'school': ('Skola')
}

SCAN_INTERVAL = timedelta(hours=4)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_VALUE_AS_TEXT, default=False): cv.boolean,
    vol.Required(CONF_SENSORS, default=[]): vol.Optional(cv.ensure_list, [vol.In(SENSOR_OPTIONS)]),
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Skolmaten sensor."""
    name    = config.get(CONF_NAME)
    sensors = config.get(CONF_SENSORS)
    devices = [];

    for sensor in sensors:
        school  = [];
        page =requests.get('https://skolmaten.se/' + sensor['school'] + '/rss/weeks/?offset=0')
        soup = BeautifulSoup(page.content, "html.parser")
        for days in soup.select('item'):
            day   = item.select('title')[0].text.strip()
            food  = item.select('description')[0].text.strip()
            date  = item.select('pubDate')[0].text
            school.append({
                'day' : day,
                'date': date,
                'food': food
            });
        devices.append(SkolmatenSensor(sensor['school'], sensor, school, hass))
    add_devices(devices, True)

# pylint: disable=no-member
class SkolmatenSensor(Entity):
    """Representation of a Skolmaten sensor."""

    page = ""
    updatedAt = datetime.now().timestamp()

    def __init__(self, name, sensor, data, hass, day=0):
        """Initialize a Skolmaten sensor."""
        self._textValue  = textValue
        self._item       = sensor
        self._school     = sensor['school']
        self._food       = data['name']
        self._day        = data['day']
        self._date       = data['date']
        self._name       = "skolmaten {}".format(name)
        self._entity_id  = generate_entity_id(ENTITY_ID_FORMAT, self._name, hass=hass)
        self._attributes = data
        self._result     = None

    @property
    def entity_id(self):
        """Return the name of the sensor."""
        return self._entity_id

    @property
    def friendly_name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""
        if self._state is not None:
            return self._state
        return None

    @property
    def device_state_attributes(self):
        """Return the state attributes of the monitored installation."""
        if self._attributes is not None:
            return self._attributes

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return ""

    @property
    def icon(self):
        """ Return the icon for the frontend."""
        return 'mdi:food'

    def update(self):
        #update values
        if not SkolmatenSensor.page or (datetime.now().timestamp() - Skolmaten.updatedAt) >= (3600*4):
            SkolmatenSensor.page      = requests.get('https://skolmaten.se/' + self._school + '/rss/weeks/?offset=0')
            SkolmatenSensor.updatedAt = datetime.now().timestamp()
        self._result     = BeautifulSoup(SkolmatenSensor.page.content, "html.parser")
        self._attributes = {}

        soup = BeautifulSoup(page.content, "html.parser")
        for days in soup.select('item'):
            day   = item.select('title')[0].text.strip()
            food  = item.select('description')[0].text.strip()
            date  = item.select('pubDate')[0].text
            school.append({
                'day' : day,
                'date': date,
                'food': food
            });
        self._state = sys.getsizeof(school)
        self._attributes.update({"day": day})
        self._attributes.update({"date": date})
        self._attributes.update({"food": food})