from django.shortcuts import render,redirect
from .models import URLModel
from django.http import HttpResponseForbidden

def dashboard_view(request):
        # print("AUTH CLASSES:", request.authenticators)
        print("COOKIES:", request.COOKIES)
        print("USER:", request.user)
        return render(request,"url_short/dashboard.html")

def url_result(request,shorten_url):
    # print("AUTH CLASSES:", request.authenticators)
    print("COOKIES:", request.COOKIES)
    print("USER:", request.user)
    if request.method == 'GET':
        url = URLModel.objects.get(shorten_url = shorten_url,user=request.user)
        if not url:
            return HttpResponseForbidden('url not found')
        url.clicks += 1 
        url.save()
        print(url)
        print(shorten_url)
        return redirect(url.original_url)
