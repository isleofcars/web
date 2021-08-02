from django import template

register = template.Library()

@register.filter(name='as_list_of_str')
def as_list_of_str(value: str, key: str = ',') -> list:
  """Returns the value turned into a list."""
  value = value.lstrip('(').lstrip('[').rstrip(')').rstrip(']')
  value = [x.strip('\"') for x in value.split(key)]
  return value


@register.filter(name='pop')
def pop(value: list, key: int = -1):
  """Returns the value by index."""
  return value[int(key)]
