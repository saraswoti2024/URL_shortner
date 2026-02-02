from django.urls import path
from .views import *
urlpatterns = [
    path('dashboard/',dashboard_view,name="dashboard"),
    path('<str:shorten_url>/',url_result,name="url")
]