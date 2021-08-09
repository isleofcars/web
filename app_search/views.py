import json
import time

import django
from django.shortcuts import render
from django.db import connection
import pandas as pd
# from django.contrib.gis.utils import GeoIP
import requests

from . import sql_queries


def get_location(request):

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    url = 'http://ipinfo.io/{ip}/json'
    response = requests.get(url.format(
        ip=get_client_ip(request)
    )).text
    location = json.loads(response)
    # My home in Bakersfiled
    my_home_coordinates = '35.40949754729655,-118.93465648638583'
    latitude, longitude = location.get('loc', my_home_coordinates).split(',', 1)
    latitude, longitude = float(latitude), float(longitude)
    return latitude, longitude


def render_search_page(request: django.http.request.HttpRequest) -> render:
    """Renders the main search page of the website."""
    per_page = 25
    conditions = ''
    if request.method == 'GET':
        print(request.GET)
        page = int(request.GET.get('page', 1))
        condition = request.GET.get('condition')
        make = request.GET.get('make')
        model = request.GET.get('model')
        body = request.GET.get('body')
        transmission = request.GET.get('transmission')
        drive = request.GET.get('drive')
        year_min = request.GET.get('year_min')
        year_max = request.GET.get('year_max')
        mileage_min = request.GET.get('mileage_min')
        mileage_max = request.GET.get('mileage_max')
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        latitude, longitude = get_location(request)
        # Extend the conditions with filter values
        if condition: conditions += f'and condition = \'{condition}\'\n'
        if make: conditions += f'and make = \'{make}\'\n'
        if model: conditions += f'and model = \'{model}\'\n'
        if body: conditions += f'and body = \'{body}\''
        if transmission: conditions += f'and transmission = \'{transmission}\'\n'
        if drive: conditions += f'and drive = \'{drive}\'\n'
        # print('page', page)
        # print('latitude, longitude', latitude, longitude)
        makes = pd.read_sql(sql_queries.makes_for_filter, connection)['make'].tolist()    # TODO: Take it from my library. or change the query - sort by quantity of ads (show ~50 most popular makes (in alphabet order))
        makes.sort()
        bodies = [
            'Hatchback',
            'Coupe',
            'Convertible',
            'Sedan',
            'SUV',
            'Pickup Truck',
            'Commercial',
            'Minivan',
            'Wagon'
        ]
        transmissions = [
            'Automatic',
            'Manual'
        ]
        drives = [
            'AWD',
            'RWD',
            'FWD'
        ]
        total_query = sql_queries.total_by_filters.format(conditions='')
        total = pd.read_sql(total_query, connection).iloc[0, 0]
        total = f'{total:,.0f}'
        ads_query = sql_queries.ads_by_filters.format(
            latitude=latitude,
            longitude=longitude,
            conditions=conditions,
            offset=page * per_page,
            per_page=per_page
        )
        print(ads_query)
        t_s = time.time()
        ads = pd.read_sql(ads_query, connection)
        print(f'Fetched results in {time.time() - t_s}')
        # Get ready for the rendering
        ads['price'] = ads.price.apply(lambda x: f'${x:,.0f}' if x else 'Priceless')
        print(ads[ads.year.isna()])
        ads['year'] = ads.year.astype(int)
        ads['power'] = ads.power.apply(lambda x: f'{x:,.0f} hp' if x else '')
        ads['mileage'] = ads.mileage.apply(lambda x: f'{x:,.0f} mi' if x else '')
        ads = ads.fillna('')
        # drives = {
        #     'FWD': 'Front-wheel drive',
        #     'RWD': 'Rear-wheel drive',
        #     'AWD': 'All-wheel drive'
        # }
        # ads['drive_title'] = ads.drive.apply(lambda x: drives.get(x, ''))

        # todo: make only one function for this
            # df = df.apply(transform_row, axis=1)
            # + make title here instead of model & make
        filters = dict(
            page=page,
            condition=condition,
            makes=makes,
            bodies=bodies,
            transmissions=transmissions,
            drives=drives
        )
        if request.is_ajax():
            return render(
                request=request,
                template_name='search_page_results.html',
                context=dict(
                    ads=ads,
                    # filters=filters,
                    # total=total
                )
            )
        return render(
            request=request,
            template_name='search_page.html',
            context=dict(
                ads=ads,
                filters=filters,
                total=total
            )
        )
