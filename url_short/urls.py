from django.urls import path
from .views import *
urlpatterns = [
    path('dashboard/',dashboard_view,name="dashboard"),
    path('<str:shorten_url>/',url_result,name="url"),
    path('get_url/<str:shorten_url>/', get_url_info, name="get_url_info"),
]