from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import uuid

class User(AbstractUser):
    bio = models.TextField(blank=True, verbose_name='بیوگرافی')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='تصویر پروفایل')
    is_email_verified = models.BooleanField(default=False, verbose_name='ایمیل تایید شده')
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Username validation - only letters, numbers, and underscores
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='نام کاربری فقط می‌تواند شامل حروف، اعداد و خط زیر باشد.'
            )
        ],
        verbose_name='نام کاربری'
    )
    
    # Email validation - override the default email field
    email = models.EmailField(
        unique=True,
        verbose_name='ایمیل',
        help_text='ایمیل معتبر وارد کنید'
    )
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
    
    def __str__(self):
        return self.username

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE, verbose_name='دنبال کننده')
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE, verbose_name='دنبال شونده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = 'دنبال کردن'
        verbose_name_plural = 'دنبال کردن‌ها'

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"