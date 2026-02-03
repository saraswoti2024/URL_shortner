from url_short.models import URLModel
from rest_framework import serializers
import hashlib
from accounts.models import CustomUser
import string

BASE62 = string.digits + string.ascii_lowercase + string.ascii_uppercase

def encode_base62(num):
    if num == 0:
        return BASE62[0]
    base62 = []
    while num > 0:
        num, rem = divmod(num, 62)
        base62.append(BASE62[rem])
    return ''.join(reversed(base62))

class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLModel
        fields = ['original_url', 'shorten_url', 'clicks']
        read_only_fields = ['shorten_url', 'clicks']
        

    def create(self,validated_data):
        user = validated_data.pop("user")
        print(user,'-------------------------------------------------')
 
        original_url = validated_data['original_url']

        value , created = URLModel.objects.get_or_create(original_url=original_url,user=user)
        value.shorten_url = encode_base62(value.id)
        value.save(update_fields=['shorten_url'])
        print(value,'------------')
        return value
