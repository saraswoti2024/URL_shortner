from rest_framework import serializers
from ..models import CustomUser,EmailVerification
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import uuid

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(validators=[])  # removes UniqueValidator
    class Meta:
        model = CustomUser
        fields = ['full_name','email','password','password1']
        validators = []
    
    def validate_email(self,value):
        user =  CustomUser.objects.filter(email=value).first()
        if user:
            if user.is_email_verified:
                raise serializers.ValidationError("email already exists try login!")
            else:
                raise serializers.ValidationError("email exists but is not verified, verify first!")
        return value
        
    
    def validate(self,data):
        try:
            validate_password(data["password"])
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password_error' :e.messages})
        if data.get('password') != data.get('password1'):
            raise serializers.ValidationError('password and password1 didn\'t match')
        return data
    
    def create(self,validated_data):
        validated_data.pop('password1')
        passwords = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(passwords)
        user.save()
        return user

class EmailverificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerification
        fields = '__all__'
        read_only_fields = ['token','expires_at','created_at']


class Emailverify(serializers.Serializer):
    token = serializers.UUIDField(required=True)

class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
    
        token['email'] = user.email
        token['is_email_verified'] = user.is_email_verified
        token['user_id'] = user.id

        return token
    
    def validate(self,attrs):
        data = super().validate(attrs)
        if not self.user.is_email_verified:
            raise serializers.ValidationError({'email':'email is not verified!verify first'})
        return data
    
