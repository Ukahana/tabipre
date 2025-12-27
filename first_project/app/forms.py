from django import forms
from .models import User
from django.contrib.auth.password_validation import validate_password


class ResistForm(forms.ModelForm):
    #確認用パスワード
    password2 = forms.CharField(label='確認用パスワード', widget=forms.PasswordInput)
    
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
        #パスワード一致チェック
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("パスワードが一致しません。")

        return cleaned_data
       
        #保存処理
    def save(self,commit=False):
        user = super().save(commit=False)
        #パスワードの強度チェック
        validate_password(self.cleaned_data['password'],user)
        #問題なければパスワードを保存
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
    
class UserLoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
 