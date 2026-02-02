from django.urls import path
from .views import *
urlpatterns = [
    path('create_url/',CreateURL.as_view(),name="create_short_url"),
    path('redirect/<str:shorten_url>/',CreateURL.as_view(),name="create_short_url")
]