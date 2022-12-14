from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from django.db.models import FloatField, Value

from .models import CarAdvertisement
from .utils import get_ip_details, get_client_ip, get_locations_nearby_coords

import logging
logger = logging.getLogger(__name__)


DRIVE_CHOICES = [(x, x) for x in (
    'AWD', 'RWD', 'FWD'
)]

TRANSMISSION_CHOICES = [(x, x) for x in (
    'Automatic', 'Manual'
)]

BODY_CHOICES = [(x, x) for x in (
    'Hatchback',
    'Coupe',
    'Convertible',
    'Sedan',
    'SUV',
    'Pickup',
    'Commercial',
    'Minivan',
    'Wagon'
)]

COLOR_CHOICES = (
    ('black', 'black'),
    ('white', 'white'),
    ('gray', 'gray'),
    ('blue', 'blue'),
    ('red', 'red'),
    ('green', 'green'),
    ('yellow', 'yellow'),
    ('orange', 'orange'),
    ('brown', 'brown'),
)


class CarAdFilter(filters.FilterSet):
    """Filter with no city and distance."""
    price_from = filters.NumberFilter(field_name="price", method="price_from_exclude_zero")
    price_to = filters.NumberFilter(field_name="price", method="price_to_exclude_zero")
    year_from = filters.NumberFilter(field_name="year", lookup_expr='gte')
    year_to = filters.NumberFilter(field_name="year", lookup_expr='lte')
    mileage_from = filters.NumberFilter(field_name="mileage", lookup_expr='gte')
    mileage_to = filters.NumberFilter(field_name="mileage", lookup_expr='lte')
    power_from = filters.NumberFilter(field_name="power", method="power_from_exclude_zero")
    power_to = filters.NumberFilter(field_name="power", method="power_to_exclude_zero")
    drive = filters.MultipleChoiceFilter(choices=DRIVE_CHOICES)
    transmission = filters.ChoiceFilter(choices=TRANSMISSION_CHOICES)
    body = filters.MultipleChoiceFilter(choices=BODY_CHOICES)
    only_with_photo = filters.BooleanFilter(field_name="photos", method="has_photos", label="Only with photo")
    color = filters.MultipleChoiceFilter(choices=COLOR_CHOICES, lookup_expr='icontains')

    def price_from_exclude_zero(self, queryset, name, value):
        # filters price from the value, excluding zero
        return queryset.exclude(price=0).filter(price__gte=value)

    def price_to_exclude_zero(self, queryset, name, value):
        # filters price to the value, excluding zero
        return queryset.exclude(price=0).filter(price__lte=value)

    def power_from_exclude_zero(self, queryset, name, value):
        # filters power from the value, excluding zero
        return queryset.exclude(power=0).filter(power__gte=value)

    def power_to_exclude_zero(self, queryset, name, value):
        # filters power to the value, excluding zero
        return queryset.exclude(power=0).filter(power__lte=value)

    def has_photos(self, queryset, name, value):
        """Excludes ads without photos for only_with_photos field."""
        return queryset.exclude(photos__isnull=True).exclude(photos__exact=[]) if value else queryset

    class Meta:
        model = CarAdvertisement
        fields = ['is_new', 'is_broken', 'make', 'model']


class DistanceOrderingFilter(OrderingFilter):
    """Orders queryset by given params or by distance
    and filter by city."""

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        request_latitude = request.query_params.get('latitude', None)
        request_longitude = request.query_params.get('longitude', None)
        request_city = request.query_params.get('location', None)
        distance = request.query_params.get('distance', None)
        ordering_in_query = request.query_params.get('ordering', None)
        if request_latitude and request_longitude and request_city:
            latitude, longitude, city = request_latitude, request_longitude, request_city.split(',')[0]
            logger.info(f'city: {city}. From request')
        else:
            ip_data = get_ip_details(get_client_ip(request))
            latitude, longitude, city = ip_data.latitude, ip_data.longitude, ip_data.city
            logger.info(f'city: {city}. Found by IP')
        logger.info('{} {}'.format(city, request.META['QUERY_STRING']))
        distance = 100000 if distance == 'Any' else distance
        queryset = get_locations_nearby_coords(queryset, latitude, longitude, distance, city)
        if ordering_in_query == 'distance':
            queryset = queryset.order_by("distance")
        else:
            try:
                if "price" in ordering[0]:  # ordering is a list
                    queryset = queryset.exclude(price=0)
            except TypeError:
                pass  # It's ordering by distance
            queryset = super(DistanceOrderingFilter, self).filter_queryset(request, queryset, view)
        return queryset
