from django.contrib import admin
from django.urls import path
import home.views
import api_search.views
import analytics.views
import accounts.views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

app_name = "home"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', api_search.views.search_home, name='search_home'),
    path('cves/<str:cpe>/', api_search.views.get_cve_form_cpe, name='get_cve_form_cpe'),
    path('analytics/', analytics.views.analytics_home, name='analytics_home'),
    path('cvss-data/', analytics.views.get_data, name='get-data'),
    path("", accounts.views.login_request, name="login"), # 로그인 페이지
    path("home/", home.views.home, name="home"), # 홈 화면 페이지
    path('register/', accounts.views.register_request, name='register'),
    path('cvss-data/<str:cpe>/', analytics.views.get_data, name='get_cve_form_cpe'),
    path('cve-info/<str:cve_id>/', analytics.views.cve_info, name='cve_info'),
    path('cve-details/', TemplateView.as_view(template_name='cve_detail.html'), name='cve_details'),
    path('logout/', LogoutView.as_view(next_page='/home'), name='logout'),  
]
