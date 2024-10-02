from django.contrib import admin
from django.urls import path
import home.views
import api_search.views
import analytics.views
import analytics.views
from django.views.generic import TemplateView

urlpatterns = [
    path('', home.views.home),
    path('admin/', admin.site.urls),
    path('search/', api_search.views.search_home, name='search_home'),
    path('analytics/', analytics.views.analytics_home, name='analytics_home'),
    path('cvss-data/', analytics.views.get_data, name='get-data'),
    path('cve-info/<str:cve_id>/', analytics.views.cve_info, name='cve_info'),
    path('cve-details/', TemplateView.as_view(template_name='cve_detail.html'), name='cve_details'),
]

