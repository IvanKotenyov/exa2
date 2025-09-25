from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, ActivationCode


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password_confirm')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Сериализатор для входа пользователя"""
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            
            if not user:
                raise serializers.ValidationError('Неверные учетные данные')
            
            if not user.is_active:
                raise serializers.ValidationError('Аккаунт не активирован')
            
            attrs['user'] = user
            return attrs
        
        raise serializers.ValidationError('Email и пароль обязательны')


class ActivationSerializer(serializers.Serializer):
    """Сериализатор для активации аккаунта"""
    
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    
    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден')
        
        if user.is_active:
            raise serializers.ValidationError('Аккаунт уже активирован')
        
        try:
            activation_code = ActivationCode.objects.get(user=user)
        except ActivationCode.DoesNotExist:
            raise serializers.ValidationError('Код активации не найден')
        
        if activation_code.is_expired():
            raise serializers.ValidationError('Код активации истек')
        
        if activation_code.code != code:
            raise serializers.ValidationError('Неверный код активации')
        
        attrs['user'] = user
        attrs['activation_code'] = activation_code
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для информации о пользователе"""
    
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined')
        read_only_fields = ('id', 'date_joined')