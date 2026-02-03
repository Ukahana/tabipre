from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from ..models import User
import re

UserModel = get_user_model()


# ============================
#  登録フォーム
# ============================
class RegistForm(forms.ModelForm):
    label_suffix = ""

    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='パスワード(確認)',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['user_name', 'email']
        labels = {
            'user_name': '名前/ニックネーム',
            'email': 'メールアドレス',
        }
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'oninput': 'this.value = this.value.toLowerCase();'
            }),
        }

    # --- ユーザー名チェック ---
    def clean_user_name(self):
        name = self.cleaned_data.get("user_name", "").strip()

        if not name:
            raise ValidationError("名前を入力してください。")

        if len(name) < 2:
            raise ValidationError("ユーザー名は2文字以上で入力してください。")

        # 絵文字OK。ただし「絵文字だけの名前」はNG
        if not re.search(r"[A-Za-z0-9ぁ-んァ-ヶ一-龠々]", name):
            raise ValidationError("ユーザー名に1文字以上の日本語・英字・数字を含めてください。")

        return name

    # --- メールアドレス正規化 + 重複チェック ---
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            return email

        email = email.strip().lower()

        if User.objects.filter(email=email).exists():
            raise ValidationError("このメールアドレスは既に登録されています。")

        return email

    # --- パスワードチェック ---
    def validate_password_rules(self, pw):
        rules = [
            (len(pw) < 10, "パスワードは10文字以上で入力してください。"),
            (not any(c.isdigit() for c in pw), "数字を1つ以上含めてください。"),
            (not any(c.islower() for c in pw), "小文字を含めてください。"),
            (not any(c.isupper() for c in pw), "大文字を含めてください。"),
        ]
        for condition, message in rules:
            if condition:
                self.add_error('password', message)

        try:
            validate_password(pw)
        except ValidationError as e:
            self.add_error('password', e)

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get("password")
        pw2 = cleaned.get("password2")

        if pw and pw2 and pw != pw2:
            self.add_error('password2', "パスワードが一致しません。")

        if pw:
            self.validate_password_rules(pw)

        return cleaned

    # --- 保存処理 ---
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


# ============================
#  ログインフォーム
# ============================
class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label='メールアドレス',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'oninput': 'this.value = this.value.toLowerCase();'
        }),
        error_messages={
            'required': 'メールアドレスを入力してください。',
            'invalid': '正しいメールアドレスを入力してください。',
        }
    )
    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'パスワードを入力してください。'}
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            email = email.strip().lower()
        return email


# ============================
#  パスワード再設定フォーム（カスタム）
# ============================
class CustomPasswordResetForm(PasswordResetForm):

    email = forms.EmailField(
        label="メールアドレス",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'oninput': 'this.value = this.value.toLowerCase();'
        }),
        error_messages={
            'required': 'メールアドレスを入力してください。',
            'invalid': '正しいメールアドレスを入力してください。',
        }
    )

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()

        if not UserModel.objects.filter(email=email).exists():
            raise ValidationError("このメールアドレスは登録されていません。")

        return email