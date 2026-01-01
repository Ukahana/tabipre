from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from ..models import User


class RegistForm(forms.ModelForm):
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    password2 = forms.CharField(label='パスワード(確認用)', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['user_name','email']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'user_name': '名前/ニックネーム',
            'email': 'メールアドレス',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("パスワードが一致しません。")
        # 大文字・小文字チェック
        if password:
            if not any(c.islower() for c in password):
                self.add_error('password', "パスワードには小文字を含めてください。")

            if not any(c.isupper() for c in password):
                self.add_error('password', "パスワードには大文字を含めてください。")

            try:
                validate_password(password)
            except ValidationError as e:
                self.add_error('password', e)

        return cleaned_data

        #保存処理
    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())