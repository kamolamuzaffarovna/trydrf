from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from account.models import User
from django.contrib.auth.password_validation import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=221, validators=[validate_password], write_only=True)
    password2 = serializers.CharField(max_length=221, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return str(token.key)

    class Meta:
        model = User
        fields = ['username', 'token', 'password1', 'password2']

    def validators(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if password1 != password2:
            raise ValidationError({'password2': 'Passwords did not match'})
        return attrs

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        password2 = validate_password('password2')
        user = super().create(validated_data)
        user.set_password(password2)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'last_login', 'created_date']