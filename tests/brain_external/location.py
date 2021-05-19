from random import getrandbits

import logging
import requests

logger = logging.getLogger(__name__)


class Location(object):
    """Location on Earth"""

    UNKNOWN = "Unknown"

    def __init__(self):
        # TODO use UUIDs
        self._id = getrandbits(128)
        self._label = self.UNKNOWN

        try:
            loc = requests.get("https://ipinfo.io").json()

            self._country = loc['country']  # pycountry.countries.get(alpha_2=loc['country']).name
            self._region = loc['region']
            self._city = loc['city']
        except:
            self._log = logger.getChild(self.__class__.__name__)
            self._log.exception("Failed to get location information")
            self._country = self.UNKNOWN
            self._region = self.UNKNOWN
            self._city = self.UNKNOWN

    @property
    def id(self):
        # type: () -> int
        """
        ID for this Location object

        Returns
        -------
        id: int
        """
        return self._id

    @property
    def country(self):
        # type: () -> str
        """
        Country String

        Returns
        -------
        country: str
        """
        return self._country

    @property
    def region(self):
        # type: () -> str
        """
        Region String

        Returns
        -------
        region: str
        """
        return self._region

    @property
    def city(self):
        # type: () -> str
        """
        City String

        Returns
        -------
        city: str
        """
        return self._city

    @property
    def label(self):
        # type: () -> str
        """
        Learned Location Label

        Returns
        -------
        label: str
        """
        return self._label

    @label.setter
    def label(self, value):
        # type: (str) -> None
        """
        Learned Location Label

        Parameters
        ----------
        value: str
        """
        self._label = value

    def __repr__(self):
        return "{}({}, {}, {})".format(self.__class__.__name__, self.city, self.region, self.country)
