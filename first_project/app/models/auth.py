from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

class UserManager(BaseUserManager):
    def create_user(self,email,user_name, password=None):
        if not user_name:
            raise ValueError('ユーザーネームを入力してください')
        if not email:
            raise ValueError('メールアドレスを入力してください')

        email = self.normalize_email(email)

        user = self.model(
            user_name=user_name,
            email=email,
            is_active=True,
        )
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self,email,user_name, password=None):
        user = self.create_user(
            email=email,
            user_name=user_name,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        
        if not user.is_staff:
         raise ValueError('Superuser must have is_staff=True.')
        if not user.is_superuser:
         raise ValueError('Superuser must have is_superuser=True.')
        
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(
        primary_key=True,
        verbose_name=_("ユーザーID")
    )
    user_name = models.CharField(
        max_length=64,
        verbose_name=_("ユーザー名")
        )
    email = models.EmailField(
        max_length=128,unique=True,
         verbose_name=_("メールアドレス")
        )
    
    # password フィールドは自前で定義しない。
    
    created_at = models.DateTimeField(
         auto_now_add=True,
         verbose_name=_("作成日")
         )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("更新日")
        )

    # Django 標準フィールド
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    objects = UserManager()

    def get_absolute_url(self):
        return reverse_lazy('app:user_login')
