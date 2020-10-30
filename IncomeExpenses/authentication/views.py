from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics,views
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer,EmailVerificationSerializer
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .Util import Util
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        serializer=self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
        user1=User.objects.get(email=user_data['email'])
        token=RefreshToken.for_user(user1).access_token
        current_site=get_current_site(request).domain
        relativeLink=reverse('email-verify')
        absUrl='http://'+current_site+relativeLink+"?token="+str(token)
        email_body="Hi "+user1.username+" Use the link above to verify your account \n"+absUrl
        data={'email_body':email_body,'to_email':user1.email,'email_subject':"Verify Your Account"}
        Util.send_email(data)
        return Response(user_data,status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class=EmailVerificationSerializer

    token_param_config=openapi.Parameter('token',in_=openapi.IN_QUERY,description='TOKEN',type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        token=request.GET.get('token')
        try:
            payload=jwt.decode(token,settings.SECRET_KEY)
            user=User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified=True
                user.save()
            return Response({'Success':'Email Activation Successfull'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'Error':'Token is already Expired '},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'Error':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST)
