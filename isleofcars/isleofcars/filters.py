from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()


@register.filter
def make_ad_text(ad) -> str:
    """Generate an ad description."""
    max_len = 1024
    description = ''
    if ad.mileage:
        description += f'{ad.mileage:,} mi'
    if ad.body:
        description += f', {ad.body}'
    if ad.transmission:
        description += f', {ad.transmission} transmission'
    if ad.drive:
        description += f', {ad.drive}'
    if ad.power:
        description += f', {ad.power} hp'
    if ad.description:
        description += f'. {ad.description}'
    if len(description) > 1024 + 3:
        description = description[:max_len] + '...'
    return description
