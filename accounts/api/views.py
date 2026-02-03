from django.shortcuts import render
from rest_framework.views import APIView
from accounts.api.serializers import UserSerializer,EmailverificationSerializer,Emailverify,CustomTokenSerializer
from rest_framework import status
from accounts.models import EmailVerification,CustomUser
from rest_framework.response import Response
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

 
def send_email_verification(email,url):
        send_mail(
            subject="email verification link",
            message = f"click the link to verify your email : {url} ",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,)

class EmailRegister(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                print(user,'valueeeeee')
                token_obj = EmailVerification.objects.create(user=user)
                verify_url =  "http://localhost:8000/verify-email/"f"?token={token_obj.token}"
                send_email_verification(user.email,verify_url)
                return Response({'message': "email verification send!check your mail"},status=status.HTTP_200_OK)
            return Response({'message': serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(f"{str(e)}",status=status.HTTP_400_BAD_REQUEST)

class EmailVerify(APIView):
     permission_classes = [AllowAny]
     def post(self,request):
        serializer = Emailverify(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_value = serializer.validated_data['token']
        try:
            token_obj = EmailVerification.objects.select_related("user").get(token=token_value)
        except EmailVerification.DoesNotExist:
            return Response({'error':'invalid token'},status = status.HTTP_400_BAD_REQUEST)
        if token_obj.is_expired():
            token_obj.delete()
            return Response({'error': 'token is expired!'},status=status.HTTP_400_BAD_REQUEST)
    
        user_obj = token_obj.user
        user_obj.is_email_verified = True
        user_obj.login_type = "email"
        user_obj.save()
        token_obj.delete()
        return Response({'message':'email successfully verified!'},status=status.HTTP_201_CREATED)
     
class ResendEmailVerification(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        email = request.data.get('email')
        if email :
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({'error': 'invalid email try again!'})
            if user.is_email_verified :
                return Response({'message':'already verified email! try login in!'})

            EmailVerification.objects.filter(user=user).delete()
            token_obj = EmailVerification.objects.create(user=user)
            verify_url = f"{"localhost"}/api-accounts/verify-email/?token={token_obj.token}"
            send_email_verification(user.email,verify_url)
            return Response({'message': "email verification resent!check your mail"},status=status.HTTP_200_OK)
        return Response({'error': "email is required!"},status=status.HTTP_200_OK)

class CustomToken(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        response = Response(
            {
                "message": "Login successful",
                "email": user.email,
                "is_email_verified": user.is_email_verified,
                "user_id": user.id
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="Lax",
            max_age=24*60*60,
            path="/",        
            secure=False,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="Lax",
            max_age=7*24*3600,
            path="/",        
            secure=False,
        )

        return response

class LogoutView(APIView):

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"error": "No refresh token found."}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response({"message": "Logged out successfully."})
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=400)