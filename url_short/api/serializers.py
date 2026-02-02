from url_short.models import URLModel
from rest_framework import serializers
import hashlib
from accounts.models import CustomUser


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLModel
        fields = ['original_url']

    def create(self,validated_data):
        request = self.context['request']  
        original_url = validated_data['original_url']
        short_code = hashlib.md5(original_url.encode()).hexdigest()[:6]
        value,created = URLModel.objects.get_or_create(original_url=original_url,user=request.user.id,defaults={
            'shorten_url':short_code ,
        })
        return value
