from django.urls import path
from . import views

urlpatterns = [
    # This will render the YouTube Data Checker form
    path('youtube/', views.youtube_info_view, name='youtube-info-view'),
    # if this doesn't work check if the previous address is linked somewhere
    # in the original app this was the home page 
    
    # original URL
    path('info/', views.youtube_info_view, name="youtube-info-view"),
    path('fetch-data/', views.fetch_data, name='fetch_data'),
    path('export-csv/', views.export_to_csv, name='export_csv'),
    ]
