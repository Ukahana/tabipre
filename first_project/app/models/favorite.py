from django.db import models
from .auth import User 

class Favorite(models.Model):
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