from django import template
from django.conf import settings
from routerfleet_tools.models import WebadminSettings

register = template.Library()


@register.simple_tag
def tag_webadmin_version():
    webadmin_settings, settings_created = WebadminSettings.objects.get_or_create(name='webadmin_settings')
    if webadmin_settings.current_version != settings.ROUTERFLEET_VERSION:
        webadmin_settings.current_version = settings.ROUTERFLEET_VERSION
        webadmin_settings.save()
    if webadmin_settings.current_version == webadmin_settings.latest_version:
        webadmin_settings.update_available = False
        webadmin_settings.save()
    return {
        'current_version': settings.ROUTERFLEET_VERSION / 10000,
        'latest_version': webadmin_settings.latest_version / 10000,
        'update_available': webadmin_settings.update_available,
    }
