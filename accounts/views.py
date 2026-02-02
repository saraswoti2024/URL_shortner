from django.shortcuts import render

def register_view(request):
    return render(request,"accounts/register.html")

def email_verify(request):
    return render(request,"accounts/email_verify.html")

def login_view(request):
    return render(request,"accounts/login.html")

def base_view(request):
    return render(request,"base.html")