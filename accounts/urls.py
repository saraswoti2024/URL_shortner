from django.urls import path
from .views import *
from django.http import HttpResponse
urlpatterns = [
    path('register/',register_view,name="register"),
    path('login/',login_view,name="login"),
    path('',base_view,name="base"),
    path("favicon.ico", lambda request: HttpResponse(status=204)),
]