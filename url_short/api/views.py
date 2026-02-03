from url_short.models import URLModel
from url_short.api.serializers import *
from rest_framework.views import APIView,Response,status
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated

class CreateURL(APIView):
    def post(self,request):
        serializer =  URLSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(user=request.user)
        shorter_url = request.build_absolute_uri(f'/url_short/{obj.shorten_url}/')
      
        return Response({
            'user': obj.user.id,
            'orginal_url' : obj.original_url,
            'shorten_url': shorter_url,
            'clicks' : obj.clicks,
        })
    
    def delete(self,request,shorten_url=None):
        try:
            value = URLModel.objects.get(shorten_url=shorten_url,user=request.user)
            value.delete()
            return Response({'message':'Successfully deleted'}, status=status.HTTP_200_OK)
        except URLModel.DoesNotExist:
            return Response({'error':'URL not found'}, status=status.HTTP_404_NOT_FOUND)

