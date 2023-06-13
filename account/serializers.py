from xml.dom import ValidationErr
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from  django.contrib.auth.tokens import PasswordResetTokenGenerator

# Internal 
from account.models import User
from account.utils import send_mail
import os



class UserRegistrationSerializer(ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only= True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'term', 'password2']
        extra_kwargs={
            'password':{'write_only':True}

        }
    

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2 :
            raise serializers.ValidationError("Password and Confirm password does not match")
        
        return attrs
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    





class UserLoginSerializer(ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']
        


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']



class UserChangepasswordSerializer(ModelSerializer):
    password = serializers.CharField(max_length=100, style = {'input_type':'password'}, write_only= True)
    password2 = serializers.CharField(max_length=100, style = {'input_type':'password'}, write_only= True)
    
    class Meta:
        model =User
        fields = ['password','password2']


    def  validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        if password != password2 :
            raise serializers.ValidationError("Password and Confirm password does not match")

        user.set_password(password)
        user.save()
        return attrs
    





class SendPasswordRestEmailSerializer(ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['email']
    


    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded User_id',uid)
            token = PasswordResetTokenGenerator().make_token(user=user)
            print("password reset Token",token)
            link = 'https://localhost:3000/api/user/reset/'+ uid +'/'+token


            print("password Reset Link", link)
            # send email code
            body = "Click Here to Reset Your password" +'  ' + link
            sender_Email = 'sourabhd081@gmail.com'
            password =   'qxxfsqkwerxkwhcq'
            receiver_email= user.email
            print(user.email,  password, password)
            
            subject = 'Reset Your Password'
            message = link
            send_mail(sender_email=sender_Email, sender_password=password,
                       receiver_email=receiver_email, subject=subject, message=message)
            
            return attrs

      
        else:
            raise ValidationErr('You are not a register user')
        
    


class UserpasswordResetSerializer(ModelSerializer):
    password = serializers.CharField(max_length=100, style = {'input_type':'password'}, write_only= True)
    password2 = serializers.CharField(max_length=100, style = {'input_type':'password'}, write_only= True)
    
    class Meta:
        model =User
        fields = ['password','password2']


    def  validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token =self.context.get('token')
            


            if password != password2 :
                raise serializers.ValidationError("Password and Confirm password does not match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationErr('Token is not valid or expired')
            
            user.set_password(password)
            user.save()
            return  attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationErr('Token is not valid or expired')