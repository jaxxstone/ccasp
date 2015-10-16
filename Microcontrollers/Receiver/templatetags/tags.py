from django import template
import re
from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag
def hello_world():
    return u'Hello world'


@register.simple_tag(takes_context=True)
def active_page(context, pattern_or_urlname):
    try:
        pattern = '^' + reverse(pattern_or_urlname) + '$'
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''
    
    