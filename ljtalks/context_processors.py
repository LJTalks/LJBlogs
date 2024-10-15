from django.contrib.auth.models import Group


def add_is_tester(request):
    is_tester = False
    if request.user.is_authenticated:
        is_tester = request.user.groups.filter(name='testers').exists()
    return {'is_tester': is_tester}
