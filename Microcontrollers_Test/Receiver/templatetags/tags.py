from django import template

register = template.Library()

@register.simple_tag
def hello_world():
    return u'Hello world'


@register.simple_tag
def active_page(request, *view_name):
    from django.core.urlresolvers import resolve, Resolver404
    if not request:
        return ""
    
    try:
        result = ""
        for view in view_name:
            
            if resolve(request.path_info).url_name == view:
                result += "panel-collapse collapse in"
            else:
                result += ""
        
        if result == "":
            result = "panel-collapse collapse"
        
        return result
    except Resolver404:
        return ""