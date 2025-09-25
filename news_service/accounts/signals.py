from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from .models import User, ActivationCode


@receiver(post_save, sender=User)
def create_activation_code(sender, instance, created, **kwargs):
    """
    Сигнал для создания кода активации при регистрации пользователя
    """
    if created and not instance.is_superuser:
        # Генерируем 6-значный код активации
        code = ''.join(random.choices(string.digits, k=6))
        
        # Создаем код активации
        ActivationCode.objects.create(user=instance, code=code)
        
        # Отправляем email с кодом активации
        subject = 'Активация аккаунта'
        message = f'''
        Добро пожаловать в News Service!
        
        Для активации вашего аккаунта используйте код: {code}
        
        Код действителен в течение 24 часов.
        
        Email для активации: {instance.email}
        '''
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=False,
            )
            print(f"Письмо с кодом активации отправлено на {instance.email}")
        except Exception as e:
            print(f"Ошибка отправки письма: {e}")


@receiver(post_save, sender=User)
def user_activated(sender, instance, **kwargs):
    """
    Сигнал для удаления кода активации после активации пользователя
    """
    if instance.is_active:
        try:
            activation_code = ActivationCode.objects.get(user=instance)
            activation_code.delete()
            print(f"Код активации для {instance.email} удален после активации")
        except ActivationCode.DoesNotExist:
            pass