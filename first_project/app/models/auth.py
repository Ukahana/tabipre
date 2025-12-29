from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.urls import reverse_lazy

class UserManager(BaseUserManager):
    def create_user(self, user_name, email, password=None):
        if not user_name:
            raise ValueError('ユーザーネームを入力してください')
        if not email:
            raise ValueError('メールアドレスを入力してください')

        email = self.normalize_email(email)

        user = self.model(
            user_name=user_name,
            email=email,
        )
        user.set_password(password)  # password_hash に自動でハッシュが入る
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, email, password=None):
        user = self.create_user(user_name, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=128,unique=True)
    password_hash = models.CharField(max_length=128,blank=True)  # AbstractBaseUser の password を上書き
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Django 標準フィールド
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    objects = UserManager()

    def save(self, *args, **kwargs):
        # AbstractBaseUser の password を password_hash に同期
        if self.password and self.password != self.password_hash:
            self.password_hash = self.password
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('app:user_login')
