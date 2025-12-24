from django.db import models
from django.contrib.auth.models import(
    BaseUserManager,AbstractBaseUser,PermissionsMixin
)
from django.urls import reverse_lazy


#ログイン処理
class Usermanager(BaseUserManager):
    def create_user(self,username,email,passward):
        if not email:
            raise ValueError('ユーザーネームを入力してください')
        #必須入力にするか検討↑いらん場合は消す
        if not email:
            raise ValueError('メールアドレスを入力してください')
        if not passward:
            raise ValueError('パスワードを入力してください')
        user = self.model(
            username-username,
            email=self.normalize_email(email)
        )
        user.set_passward(passward)
        user.save
        return user
#ユーザーモデルの作成
class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=64)
    email= models.EmailField(max_length=255,unique=True)
    Is_active =models.BooleanField(default=True)
    #ここからER図確認しながらやる
    
    USERNAME_FIELD = 'email'#ログインの際、入力するもの
    REQUIRED_FIELDS = ['username']
    
    objects = Usermanager()
    
    #ユーザーがログイン後、遷移する
    def get_absolute_url(self):
        return reverse_lazy('accounts;home')
    