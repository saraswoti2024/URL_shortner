from django.shortcuts import render,redirect,get_object_or_404
from .models import URLModel
from django.http import HttpResponseForbidden,JsonResponse

def dashboard_view(request):
        # print("AUTH CLASSES:", request.authenticators)
        print("COOKIES:", request.COOKIES)
        print("USER:", request.user)
        return render(request,"url_short/dashboard.html")

def url_result(request,shorten_url):
    if request.method == 'GET':
        url = URLModel.objects.get(shorten_url = shorten_url)
        if not url:
            return HttpResponseForbidden('url not found')
        url.clicks += 1 
        print(url.clicks)
        url.save()
        print(url)
        print(shorten_url)
        return redirect(url.original_url)


def get_url_info(request, shorten_url):
    if request.method == 'GET':
        url = get_object_or_404(URLModel, shorten_url=shorten_url)
        data = {
            'original_url': url.original_url,
            'shorten_url': url.shorten_url,
            'clicks': url.clicks,
            'created_at': url.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        return JsonResponse(data)