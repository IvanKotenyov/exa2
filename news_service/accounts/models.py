from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
from django.db import models
import uuid
from django.utils import timezone


class UserManager(BaseUserManager):
    """Менеджер для кастомной модели пользователя"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя с email в качестве логина"""
    
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=150, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='Фамилия')
    
    is_active = models.BooleanField(default=False, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
    
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()


class ActivationCode(models.Model):
    """Модель для кодов активации аккаунтов"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='activation_code')
    code = models.CharField(max_length=6, verbose_name='Код активации')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    
    class Meta:
        verbose_name = 'Код активации'
        verbose_name_plural = 'Коды активации'
    
    def __str__(self):
        return f'{self.user.email} - {self.code}'
    
    def is_expired(self):
        """Проверка истечения кода (24 часа)"""
        from django.utils import timezone
        from datetime import timedelta
        return timezone.now() > self.created_at + timedelta(hours=24)