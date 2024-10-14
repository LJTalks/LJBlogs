from django.shortcuts import render

# API View
def api_view(request):
    return render(request, 'api_app.html')
