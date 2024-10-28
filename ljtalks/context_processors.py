from django.contrib.auth.models import Group
from django.conf import settings


def add_is_tester(request):
    is_tester = False
    if request.user.is_authenticated:
        is_tester = request.user.groups.filter(name='testers').exists()
    return {'is_tester': is_tester}


def recaptcha_site_key(request):
    return {
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
    }


# def database_context(request):
#     return {
#         'DATABASE_NAME': settings.DATABASE_NAME,
#         'SHOW_DEV_BANNER': settings.SHOW_DEV_BANNER,
#     }
