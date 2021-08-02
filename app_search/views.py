import json

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
    latitude, longitude = location.get('loc', '41.2426,-82.6157').split(',', 1)
    latitude, longitude = float(latitude), float(longitude)
    print(f'ip: {latitude}, {longitude}')
    # todo: range all ads by distance (in sql + offset for pagination)


def render_search_page(request: django.http.request.HttpRequest) -> render:
    """Renders the main search page of the website."""
    query = """
    select *
    from web.ads
    limit 25
    """
    ads = pd.read_sql(query, connection)
    ads['year'] = ads.year.astype(int)
    # ads = ads.to_json(orient='records')

    # import pygeoip
    # gi = pygeoip.GeoIP('GeoIPCity.dat')
    # ip = gi.record_by_addr(get_client_ip(request))

    # from urllib2 import urlopen




    # g = GeoIP()
    # ip = request.META.get('REMOTE_ADDR', None)


    return render(
        request=request,
        template_name='search_page.html',
        context=dict(
            ads=ads
        )
    )
