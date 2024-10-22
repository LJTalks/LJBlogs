from django.contrib.auth.models import Group
from django.conf import settings


def add_is_tester(request):
    is_tester = False
    if request.user.is_authenticated:
        is_tester = request.user.groups.filter(name='testers').exists()
    return {'is_tester': is_tester}


def recaptcha_key(request):
    return {
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
    }