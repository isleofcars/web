from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import CarAdvertisement
from .serializers import CarAdSerializer, MakesSerializer
from .filters import CarAdFilter, DistanceOrderingFilter
from . import utils


class CarAdStandardPagination(PageNumberPagination):
    """
    Filtered and ordered queryset gets paginated
    And also if make is chosen it shows its models and counts
    """
    page_size = 25
    models = []
    makes = []

    def get_paginated_response(self, data):
        # adding field totalPages to response
        response = super(CarAdStandardPagination, self).get_paginated_response(data)
        response.data['totalPages'] = self.page.paginator.num_pages
        response.data['models'] = self.models
        response.data['makes'] = self.makes
        return response

    def paginate_queryset(self, queryset, request, view=None):
        request_page_size = request.query_params.get('items_per_page', None)
        self.page_size = int(request_page_size.split()[0]) if request_page_size else 25  # change number of ads per page
        result = super(CarAdStandardPagination, self).paginate_queryset(queryset, request)
        self.models = utils.get_models_and_count(queryset, request)  # add models and their counts if make is chosen
        self.makes = utils.get_makes_and_count(queryset, request)  # add models and their counts if make is chosen
        return result


class CarAdViewSet(viewsets.ModelViewSet):
    """
    Return filtered, ordered and paginated set of car ads
    """
    queryset = CarAdvertisement.objects.all().order_by('-id')
    serializer_class = CarAdSerializer
    pagination_class = CarAdStandardPagination
    filter_backends = (DjangoFilterBackend, DistanceOrderingFilter,)
    filterset_class = CarAdFilter
    ordering_fields = ['year', 'price']


class MinYearView(APIView):
    """
    Return min_year of all car ads for year filter
    """
    def get(self, request, format=None):
        result = {
            "min_year": utils.get_min_year()
        }
        return Response(result)


class UserCityView(APIView):
    """
    Return user city for city choice
    """
    def get(self, request, format=None):
        result = utils.get_client_location_details(request)
        return Response(result)


class CarMakesView(generics.ListCreateAPIView):
    """All car makes by alphabet order for make filter."""
    serializer_class = MakesSerializer

    def list(self, request, format=None):
        self.queryset = utils.get_makes_and_count(request)
        serializer = MakesSerializer(self.queryset, many=True)
        return Response(serializer.data)
