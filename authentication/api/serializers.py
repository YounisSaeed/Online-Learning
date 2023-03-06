# User Serializer

from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True , required = True , style={
        "input_type": "password"
    })
    password2 = serializers.CharField(style={"input_type": "password"},write_only=True,
    label="Confirm Password"
    )
    
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only":True}}
    
    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        password2 = validated_data["password2"]

        if (email and User.objects.filter(email=email).exclude(username=username).exists()):
            raise serializers.ValidationError(
                {"message":"Email must be unique !"}
            )
        if password != password2:
            raise serializers.ValidationError(
                {"message": "The password confirmation does not match."})

        user = User(username=username,email=email)
        user.set_password(password)
        user.save()

        return user

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    # tokens = serializers.SerializerMethodField()
    
    # def get_tokens(self, obj):
    #     user = User.objects.get(username=obj['username'])
    #     # return {
    #     #     'refresh': user.tokens()['refresh'],
    #     #     'access': user.tokens()['access']
    #     # }
    class Meta:
        model = User
        fields = ['password','username']#,'tokens']
    
    def validate(self, attrs):
        username = attrs.get('username','')
        password = attrs.get('password','')
        user = auth.authenticate(username=username,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'email': user.email,
            'username': user.username,
            #'tokens': user.tokens
        }

class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
