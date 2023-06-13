
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# internal
from account.serializers import (UserRegistrationSerializer, UserLoginSerializer, UserpasswordResetSerializer,
                                 
                                 UserChangepasswordSerializer, SendPasswordRestEmailSerializer )

from account.renders import UserRenderer
from account.serializers import  UserProfileSerializer



# generating token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'serializer':serializer.data, 'token':token}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserLoginview(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password= password)
            
            if user:
                token = get_tokens_for_user(user)
                return Response({"msg":"successfuly login", 'token':token}, status=status.HTTP_200_OK)
            else:
                return Response({"errors":{"non_field_errors":["email or password invalid"]}}, status=status.HTTP_400_BAD_REQUEST)
            


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        #if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserChangepasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangepasswordSerializer(data=request.data, context ={
            'user':request.user
        })

        if serializer.is_valid(raise_exception=True):
            return Response({'msg':"password chnage successfuly"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



class SendPasswordRestEmailView(APIView):
    def post(self, request, format=None):
        serializer = SendPasswordRestEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            return   Response({'msg':'password reset link has been sent please check your email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class UserpasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserpasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':"password reset successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    




