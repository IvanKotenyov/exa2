from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    ActivationSerializer,
    UserSerializer
)
from .models import User


@swagger_auto_schema(
    method='post',
    operation_description="Регистрация нового пользователя",
    request_body=UserRegistrationSerializer,
    responses={
        201: openapi.Response(
            description="Пользователь успешно зарегистрирован",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT)
                }
            )
        ),
        400: "Ошибки валидации"
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Регистрация нового пользователя"""
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    
    return Response({
        'message': 'Пользователь успешно зарегистрирован. Проверьте email для получения кода активации.',
    }, status=status.HTTP_201_CREATED)
    

@swagger_auto_schema(
    method='post',
    operation_description="Активация аккаунта пользователя",
    request_body=ActivationSerializer,
    responses={
        200: openapi.Response(
            description="Аккаунт успешно активирован",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        ),
        400: "Ошибки валидации"
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def activate(request):
    """Активация аккаунта пользователя"""
    serializer = ActivationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        activation_code = serializer.validated_data['activation_code']
        
        # Активация пользователя
        user.is_active = True
        user.save()
        
        # Удаление код активации
        activation_code.delete()
        
        return Response({
            'message': 'Аккаунт успешно активирован!'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="Вход в систему",
    request_body=UserLoginSerializer,
    responses={
        200: openapi.Response(
            description="Успешная авторизация",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT)
                }
            )
        ),
        400: "Ошибки валидации"
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Вход в систему"""
    serializer = UserLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Генерация JWT токены
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        user_data = UserSerializer(user).data
        
        return Response({
            'access': str(access),
            'refresh': str(refresh),
            'user': user_data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="Выход из системы (добавление токена в черный список)",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh токен')
        },
        required=['refresh']
    ),
    responses={
        200: "Успешный выход",
        400: "Ошибка токена"
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Выход из системы"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'message': 'Успешный выход из системы'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Ошибка при выходе из системы'
        }, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_description="Получение профиля текущего пользователя",
    responses={
        200: UserSerializer,
        401: "Не авторизован"
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Получение профиля пользователя"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)