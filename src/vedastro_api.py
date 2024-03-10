from datetime import datetime
from functools import lru_cache
import requests
from typing import Optional

from tzwhere import tzwhere
import zoneinfo


class VedAstroApi:
    def __init__(
        self,
        location: str,
        birth_datetime: str,
        datetime_fmt: str = "%d-%m-%Y %H:%M",
    ):
        location = self.get_location_geo_coordinates(location)
        if location is None:
            raise ValueError(f"Location {location} is not valid.")
        self.location = location
        self.birth_datetime = datetime.strptime(birth_datetime, datetime_fmt)

    @staticmethod
    @lru_cache
    def get_location_geo_coordinates(location: str) -> Optional[dict]:
        url = f"https://vedastroapi.azurewebsites.net/api/Calculate/LocationGeoCoordinates/LocationName/{location}/Ayanamsa/Raman"
        response = requests.get(url).json()
        if response["Status"] == "Pass":
            return response["Payload"]

    def _get_api_inputs(self) -> tuple[str, str, str]:
        location = self.location["LocationGeoCoordinates"]["Name"]
        birth_datetime = self.birth_datetime.strftime("%H:%M/%d/%m/%Y")
        timezone_str = tzwhere.tzwhere().tzNameAt(
            self.location["LocationGeoCoordinates"]["Latitude"],
            self.location["LocationGeoCoordinates"]["Longitude"],
        )
        tz = datetime.now(zoneinfo.ZoneInfo(timezone_str)).strftime('%z')
        tz = f"{tz[:-2]}:{tz[-2:]}"
        return location, birth_datetime, tz

    @lru_cache(maxsize=1)
    def get_planet_details(
        self, ayanamsa: str = "Lahiri Chitrapaksha"
    ) -> Optional[dict]:
        location, birth_datetime, tz = self._get_api_inputs()
        url = f"https://vedastroapi.azurewebsites.net/api/Calculate/AllPlanetData/PlanetName/All/Location/{location}/Time/{birth_datetime}/{tz}"
        if ayanamsa != "Lahiri Chitrapaksha":
            url += f"/Ayanamsa/{ayanamsa}"
        response = requests.get(url).json()
        if response["Status"] == "Pass":
            return response["Payload"]["AllPlanetData"]
        raise RuntimeError(response["Payload"])

    @lru_cache(maxsize=1)
    def get_house_details(
        self, ayanamsa: str = "Lahiri Chitrapaksha"
    ) -> Optional[dict]:
        location, birth_datetime, tz = self._get_api_inputs()
        url = f"https://vedastroapi.azurewebsites.net/api/Calculate/AllHouseData/HouseName/All/Location/{location}/Time/{birth_datetime}/{tz}"
        if ayanamsa != "Lahiri Chitrapaksha":
            url += f"/Ayanamsa/{ayanamsa}"
        response = requests.get(url).json()
        if response["Status"] == "Pass":
            return response["Payload"]["AllHouseData"]
        raise RuntimeError(response["Payload"])
