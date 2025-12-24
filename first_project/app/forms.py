from django import forms
from .models import User
from django.contrib.auth.password_validation import validate_password


class ResistForm(forms.ModelForm):
    #htmlにつながる画面設計と揃えたい
    class Meta:
        model = User
        fields = ['username','email','password']
        widgets = {
            'password':forms.PasswordInput(),
        }
        labels = {
            'username':'名前/ニックネーム',
            'email':'メールアドレス',
            'password':'パスワード',
        }
        #True↓になおす？
    def save(self,commit=False):
        user = super().save(commit=False)
        #パスワードの強度チェック
        validate_password(self.cleaned_data['password'],user)
        #問題なければパスワードを保存
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
    #ここから　コパの履歴コーどを見て修正する
    
    
    
    
    