from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import UserRegistrationsSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerilizer
from django.contrib.auth import authenticate
from account.renders import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
#Generate Token Maually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# Create your views here.
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = UserRegistrationsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user =  serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Success'},status.HTTP_201_CREATED)


        return Response(serializer.error_messages,status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request,format=None):
        seriaizer =  UserLoginSerializer(data = request.data)
        if seriaizer.is_valid(raise_exception=True):
            email = seriaizer.data.get('email')
            password =  seriaizer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Success'},status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_error':['Email or Password is not Valid']}},status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request,format=None):
        serializer =  UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserChangePasswordView(APIView):
    renderer_classes =  [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data)
        context={'user':request.user} 
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Change Success'},status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

class SendPasswordEmail(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer =  SendPasswordResetEmailSerilizer(data=request.data)
        if serializer.is_valid(raise_exception=True):
             return Response({'msg':'Password Reset link Send. Please check your Email'},status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request,uid,token, format=None):
        serializer =  SendPasswordResetEmailSerilizer(data=request.data)
        context = {'uid':uid,'token':token}
        if serializer.is_valid(raise_exception=True):
             return Response({'msg':'Password Reset Successfully'},status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

   

