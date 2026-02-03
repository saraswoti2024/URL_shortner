from url_short.models import URLModel
from url_short.api.serializers import *
from rest_framework.views import APIView,Response
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated

class CreateURL(APIView):
    def post(self,request):
        serializer =  URLSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(user=request.user)
        shorter_url = request.build_absolute_uri('/') + obj.shorten_url
        
        return Response({
            'user': obj.user.id,
            'orginal_url' : obj.original_url,
            'shorten_url': shorter_url,
        })

