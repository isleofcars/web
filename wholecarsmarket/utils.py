from django.http import HttpRequest
from django.conf import settings
import ipinfo

def get_user_location(request: HttpRequest) -> str:

    def get_client_ip(request: HttpRequest) -> str:
        """
        Return client's ip or some ip from Bellevue, WA if it's hosted locally
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        if ip == '127.0.0.1':
            return '104.52.6.199'
        return ip

    def get_ip_details(ip_address=None):
        """
        Return client's ip details such as city, region, country, latitude, longitude etc.
        ip_address - is taken from get_client_ip(request)
        """
        ipinfo_token = getattr(settings, "IPINFO_TOKEN", None)
        ipinfo_settings = getattr(settings, "IPINFO_SETTINGS", {})
        ip_data = ipinfo.getHandler(ipinfo_token, **ipinfo_settings)
        ip_data = ip_data.getDetails(ip_address)
        return ip_data

    def get_client_location_details(request: HttpRequest):
        """Returns client's real city and region as json."""
        ip_details = get_ip_details(get_client_ip(request))
        latitude, longitude = ip_details.loc.split(',', 1)
        result = {
            'city': ip_details.city,
            'region': ip_details.region,
            'latitude': latitude,
            'longitude':  longitude,
            'countryCode': ip_details.country,
        }
        return result

    location = get_client_location_details(request)
    location_str = location['city']
    state = ALL_STATES.get(location['region'])
    if state:
        location_str += f', {state}'
    return location_str


ALL_STATES = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
