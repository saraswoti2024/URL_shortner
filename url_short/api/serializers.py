from url_short.models import URLModel
from rest_framework import serializers
import hashlib
from accounts.models import CustomUser


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLModel
        fields = ['original_url']

    def create(self,validated_data):
        user = validated_data.pop("user")
        print(user,'-------------------------------------------------')
 
        original_url = validated_data['original_url']
        short_code = hashlib.md5(original_url.encode()).hexdigest()[:6]
        print(short_code,'--------------------')
        value , created = URLModel.objects.get_or_create(original_url=original_url,user=user,defaults={
            'shorten_url':short_code ,
        })
        print(value,'------------')
        return value
