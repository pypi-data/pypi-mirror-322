import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

import redis
import requests

API_URL = "https://api.wigle.net/api/v2/network/search"
REDIS_CACHE_EXPIRY = timedelta(hours=1)
API_RATE_LIMIT = 30  # seconds between requests

# Initialize Redis connection
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Track last API request time (initialized to allow immediate first request)
_last_request_time = time.time() - API_RATE_LIMIT


class WigleError(Exception):
    """Custom exception for Wigle-related errors"""

    pass


class NetworkType(str, Enum):
    """Network types supported by Wigle API"""

    WIFI = "WIFI"
    BT = "BT"
    CELL = "CELL"


class Encryption(str, Enum):
    """WiFi encryption types"""

    NONE = "None"
    WEP = "WEP"
    WPA = "WPA"
    WPA2 = "WPA2"
    WPA3 = "WPA3"
    UNKNOWN = "unknown"


@dataclass
class Location:
    """Represents a wireless network location with all available Wigle API fields"""

    ssid: str
    latitude: float
    longitude: float
    last_update: Optional[datetime]
    encryption: Optional[str] = None
    network_type: Optional[str] = None
    channel: Optional[int] = None
    frequency: Optional[float] = None
    qos: Optional[int] = None
    transid: Optional[str] = None
    firsttime: Optional[datetime] = None
    lasttime: Optional[datetime] = None
    country_code: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    house_number: Optional[str] = None
    road: Optional[str] = None
    address: Optional[str] = None


def get_wigle_auth() -> str:
    """Get Wigle authentication token from environment variable"""
    wigle_auth = os.getenv("WIGLE")
    if not wigle_auth:
        raise WigleError("WIGLE environment variable not set. Format should be: 'AIDxxx:yyy'")
    return wigle_auth


def enforce_rate_limit():
    """Enforce API rate limit by sleeping if needed, showing countdown"""
    global _last_request_time
    current_time = time.time()
    time_since_last_request = current_time - _last_request_time

    if time_since_last_request < API_RATE_LIMIT:
        sleep_time = API_RATE_LIMIT - time_since_last_request
        print(f"\nRate limit: waiting {sleep_time:.0f} seconds", end="", flush=True)

        # Show countdown
        for remaining in range(int(sleep_time), 0, -1):
            time.sleep(1)
            print(f"\rRate limit: waiting {remaining:2d} seconds", end="", flush=True)

        print("\rRate limit: continuing...           ")  # Clear the line

    _last_request_time = time.time()


def search_networks(
    *,
    # Location filters
    latitude_north: Optional[float] = None,
    latitude_south: Optional[float] = None,
    longitude_east: Optional[float] = None,
    longitude_west: Optional[float] = None,
    # Network filters
    ssid: Optional[str] = None,
    ssidlike: Optional[str] = None,
    network_type: Optional[NetworkType] = None,
    encryption: Optional[Encryption] = None,
    # Time filters
    on_since: Optional[datetime] = None,
    last_update: Optional[datetime] = None,
    # Result control
    results_per_page: int = 100,
    search_after: Optional[str] = None,
    # Other filters
    freenet: Optional[bool] = None,
    paynet: Optional[bool] = None,
    show_query: bool = False,
) -> Dict[str, Any]:
    """
    Search for networks using the Wigle API with full parameter support and Redis caching.
    Rate limited to one request per minute.

    Args:
        latitude_north: Northern boundary of search box
        latitude_south: Southern boundary of search box
        longitude_east: Eastern boundary of search box
        longitude_west: Western boundary of search box
        ssid: Exact SSID match
        ssidlike: SSID wildcard match
        network_type: Filter by network type (WIFI/BT/CELL)
        encryption: Filter by encryption type
        on_since: Only show networks seen on or after date
        last_update: Only show networks updated since date
        results_per_page: Number of results per page (max 100)
        search_after: Token for getting next batch of results
        freenet: Show only free networks
        paynet: Show only pay networks
        show_query: Return query bounds without results

    Returns:
        Dictionary containing search results and metadata including searchAfter token

    Raises:
        WigleError: If the WIGLE environment variable is not set or API request fails
    """
    # https://api.wigle.net/api/v2/network/search?onlymine=false&encryption=None&freenet=false&paynet=false
    try:
        # Build cache key from all parameters
        params = locals()
        cache_key = f"wigle:search:{json.dumps(params, default=str, sort_keys=True)}"

        cached_result = redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

        # Enforce rate limit before making request
        enforce_rate_limit()

        # Build API parameters
        api_params = {
            "onlymine": "false",
            "resultsPerPage": results_per_page,
        }

        # Add optional parameters if provided
        if latitude_north is not None:
            api_params["latrange1"] = latitude_south
            api_params["latrange2"] = latitude_north
            api_params["longrange1"] = longitude_west
            api_params["longrange2"] = longitude_east

        if ssid:
            api_params["ssid"] = ssid
        if ssidlike:
            api_params["ssidlike"] = ssidlike
        if network_type:
            api_params["netid"] = network_type.value
        if encryption:
            api_params["encryption"] = encryption.value
        else:
            api_params["encryption"] = "None"
        if on_since:
            api_params["onSince"] = on_since.strftime("%Y%m%d")
        if last_update:
            api_params["lastupdt"] = last_update.strftime("%Y%m%d")
        if freenet is not None:
            api_params["freenet"] = str(freenet).lower()
        if paynet is not None:
            api_params["paynet"] = str(paynet).lower()
        if search_after:
            api_params["searchAfter"] = search_after
        if show_query:
            api_params["showQuery"] = str(show_query).lower()

        # Make API request
        wigle_auth = get_wigle_auth()
        headers = {"Authorization": f"Basic {wigle_auth}"}
        response = requests.get(API_URL, params=api_params, headers=headers)
        response.raise_for_status()
        result = response.json()

        print(result)

        # Cache the result
        redis_client.setex(cache_key, int(REDIS_CACHE_EXPIRY.total_seconds()), json.dumps(result))

        return result

    except requests.exceptions.RequestException as e:
        raise WigleError(f"API request failed: {str(e)}")


def parse_network_to_location(network: Dict[str, Any]) -> Location:
    """Convert a network result from Wigle API to a Location object"""
    # Parse dates if present
    last_update = None
    firsttime = None
    lasttime = None

    if network.get("lastupdt"):
        try:
            last_update = datetime.strptime(network["lastupdt"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass

    if network.get("firsttime"):
        try:
            firsttime = datetime.strptime(network["firsttime"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass

    if network.get("lasttime"):
        try:
            lasttime = datetime.strptime(network["lasttime"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass

    return Location(
        ssid=network["ssid"],
        latitude=float(network["trilat"]),
        longitude=float(network["trilong"]),
        last_update=last_update,
        encryption=network.get("encryption"),
        network_type=network.get("type"),
        channel=network.get("channel"),
        frequency=network.get("frequency"),
        qos=network.get("qos"),
        transid=network.get("transid"),
        firsttime=firsttime,
        lasttime=lasttime,
        country_code=network.get("country"),
        city=network.get("city"),
        region=network.get("region"),
        house_number=network.get("housenumber"),
        road=network.get("road"),
        address=network.get("address"),
    )


def get_all() -> List[Location]:
    """Search for OpenRoaming networks and return list of locations.
    Rate limited to one request per minute, including pagination requests.

    Returns:
        List[Location]: List of found network locations

    Raises:
        WigleError: If the WIGLE environment variable is not set or API request fails
    """
    ssid_names = ["Adentro OpenRoaming", "OpenRoaming", "Passpoint", "PasspointAruba", "Cellular Wi-Fi Passthrough", "WBA_OpenRoaming"]
    locations: List[Location] = []

    for name in ssid_names:
        try:
            search_after = None
            while True:
                results = search_networks(
                    ssid=name, encryption=Encryption.NONE, network_type=NetworkType.WIFI, results_per_page=100, search_after=search_after
                )

                if not results or not results.get("results"):
                    break

                for network in results["results"]:
                    locations.append(parse_network_to_location(network))

                # Get searchAfter token for next batch
                search_after = results.get("searchAfter")
                if not search_after:
                    break

        except WigleError as e:
            raise WigleError(f"Error searching for {name}: {str(e)}")

    print(f"Found {len(locations)} OpenRoaming network locations")
    return locations


if __name__ == "__main__":
    locations = get_all()
    for loc in locations:
        print(f"SSID: {loc.ssid}")
        print(f"Location: ({loc.latitude}, {loc.longitude})")
        print(f"Network Type: {loc.network_type or 'N/A'}")
        print(f"Encryption: {loc.encryption or 'N/A'}")
        print(f"Last Update: {loc.last_update or 'N/A'}")
        if loc.address:
            print(f"Address: {loc.address}")
        print("-" * 50)
