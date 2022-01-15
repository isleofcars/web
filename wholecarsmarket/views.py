import json

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
import pandas as pd
from django.db import connection

from . import forms
from wholecarsmarket import utils
from wholecarsmarket import sql_queries as sql


# from .models import CarAdvertisement
# from .serializers import CarAdSerializer, MakesSerializer
# from .filters import CarAdFilter, DistanceOrderingFilter
# from .services import get_models_and_count, get_min_year, get_client_location_details, get_makes_and_count


def render_home(request: HttpRequest) -> HttpResponse:
    """Renders the main page."""

    def fetch_ads() -> pd.DataFrame:
        query = """select * from web.ads limit 25"""
        ads = pd.read_sql_query(query, connection)
        return ads

    print(request.GET)
    makes_all = pd.read_sql_query(sql.get_all_makes, connection)
    makes_all = makes_all.make.to_list()
    makes_popular = pd.read_sql_query(sql.get_popular_makes, connection)
    makes_popular = makes_popular.make.to_list()
    location_default = utils.get_user_location(request)
    print('location_default', location_default)
    is_new = request.GET.get('is_new', forms.CHOICES_IS_NEW[0][0])
    is_broken = request.GET.get('is_broken', forms.CHOICES_IS_BROKEN[1][0])
    location = request.GET.get('location', location_default)
    make = request.GET.get('make')
    model = request.GET.get('model')
    color = request.GET.get('color')
    body = request.GET.get('body')
    transmission = request.GET.get('transmission')
    drive = request.GET.get('drive')
    with_photos = request.GET.get('with_photos', True)
    power_from = request.GET.get('power_from')
    power_to = request.GET.get('power_to')
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    mileage_from = request.GET.get('mileage_from')
    mileage_to = request.GET.get('mileage_to')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    initial = dict(
        is_new=is_new,
        is_broken=is_broken,
        location=location,
        make=make,
        model=model,
        color=color,
        body=body,
        transmission=transmission,
        drive=drive,
        with_photos=with_photos,
        power_from=power_from,
        power_to=power_to,
        year_from=year_from,
        year_to=year_to,
        mileage_from=mileage_from,
        mileage_to=mileage_to,
        price_from=price_from,
        price_to=price_to
    )
    initial = {x: y for x, y in initial.items() if y or y == 0 or y is False}
    form = forms.FormFilters(initial=initial)
    print('initials', initial)
    ads = fetch_ads()
    ads = ads.reset_index()
    # ads['photos'] = ads.photos.astype(list)
    # print(ads)
    # filters = FormFilters(request.GET)
    # if request.is_ajax():
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(
            request=request,
            template_name='search/ads.html',
            context=dict(
                form=form,
                ads=ads,
                makes_all=json.dumps(makes_all),
                makes_popular=json.dumps(makes_popular)
            )
        )
    return render(
        request=request,
        template_name='search/home.html',
        context=dict(
            form=form,
            ads=ads,
            makes_all=json.dumps(makes_all),
            makes_popular=json.dumps(makes_popular)
        )
    )

#
# class CarAdStandardPagination(PageNumberPagination):
#     """
#     Filtered and ordered queryset gets paginated
#     And also if make is chosen it shows its models and counts
#     """
#     page_size = 25
#     additional_info = []
#
#     def get_paginated_response(self, data):
#         # adding field totalPages to response
#         response = super(CarAdStandardPagination, self).get_paginated_response(data)
#         response.data['totalPages'] = self.page.paginator.num_pages
#         response.data['models'] = self.additional_info
#         return response
#
#     def paginate_queryset(self, queryset, request, view=None):
#         request_page_size = request.query_params.get('items_per_page', None)
#         self.page_size = int(request_page_size.split()[0]) if request_page_size else 25  # change number of ads per page
#         result = super(CarAdStandardPagination, self).paginate_queryset(queryset, request)
#         self.additional_info = get_models_and_count(queryset, request)  # add models and their counts if make is chosen
#         return result
#
#
# class CarAdViewSet(viewsets.ModelViewSet):
#     """
#     Return filtered, ordered and paginated set of car ads
#     """
#     queryset = CarAdvertisement.objects.all().order_by('-id')
#     serializer_class = CarAdSerializer
#     pagination_class = CarAdStandardPagination
#     filter_backends = (DjangoFilterBackend, DistanceOrderingFilter,)
#     filterset_class = CarAdFilter
#     ordering_fields = ['year', 'price']
#
#
# class MinYearView(APIView):
#     """
#     Return min_year of all car ads for year filter
#     """
#     def get(self, request, format=None):
#         result = {
#             "min_year": get_min_year()
#         }
#         return Response(result)
#
#
# class UserCityView(APIView):
#     """
#     Return user city for city choice
#     """
#     def get(self, request, format=None):
#         result = get_client_location_details(request)
#         return Response(result)
#
#
# class CarMakesView(generics.ListCreateAPIView):
#     """
#     Return top 50 car makes by alphabet order for make filter
#     """
#     serializer_class = MakesSerializer
#
#     def list(self, request, format=None):
#         self.queryset = get_makes_and_count(request)
#         serializer = MakesSerializer(self.queryset, many=True)
#         return Response(serializer.data)
