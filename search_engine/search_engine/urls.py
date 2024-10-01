from django.contrib import admin
from django.urls import path
import home.views
import api_search.views
import analytics.views
import analytics.views

urlpatterns = [
    path('', home.views.home),
    path('admin/', admin.site.urls),
    path('search/', api_search.views.search_home, name='search_home'),
    path('analytics/', analytics.views.analytics_home, name='analytics_home'),
    path('cvss-data/', analytics.views.get_data, name='get-data'),
]

