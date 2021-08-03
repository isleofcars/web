import json
import time

import django
from django.shortcuts import render
from django.db import connection
import pandas as pd
# from django.contrib.gis.utils import GeoIP
import requests


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
    total = 25
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        print(f'page: {page}')
        latitude, longitude = get_location(request)
        print(latitude, longitude)
        # todo: range all ads by distance (in sql + offset for pagination)

        sql_query = """
        select
            *,
            coalesce(ACOS(SIN(latitude * 3.14159 / 180) * SIN({latitude} * 3.14159 / 180) + COS(latitude * 3.14159 / 180) * COS({latitude} * 3.14159 / 180) * COS((longitude - {longitude}) * 3.14159 / 180)), 99999) as distance
        from web.ads
        ORDER BY distance asc
        limit {offset}, {total};
        """
        query = sql_query.format(
            latitude=latitude,
            longitude=longitude,
            total=total,
            offset=page * total
        )
        print(query)
        t_s = time.time()
        ads = pd.read_sql(query, connection)
        print(f'Fetched results in {time.time() - t_s}')
        ads['price'] = ads.price.apply(lambda x: f'${x:,.0f}' if x else 'No price')
        print(ads[ads.year.isna()])
        ads['year'] = ads.year.astype(int)
        ads['mileage'] = ads.mileage.apply(lambda x: f'{x:,.0f} miles')
        return render(
            request=request,
            template_name='search_page.html',
            context=dict(
                ads=ads,
                page=page
            )
        )
