from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from ..models import User
import re
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm

UserModel = get_user_model()

# ============================
#  共通ユーザー名バリデーション
# ============================
def validate_user_name_common(name):
    name = name.strip()

    if not name:
        raise ValidationError("名前を入力してください。")

    if len(name) < 2:
        raise ValidationError("ユーザー名は2文字以上で入力してください。")

    # 絵文字OK。ただし「絵文字だけの名前」はNG
    if not re.search(r"[A-Za-z0-9ぁ-んァ-ヶ一-龠々]", name):
        raise ValidationError("日本語・英字・数字を1文字以上含めてください。")

    return name


def validate_email_common(email):
    email = email.strip().lower()

    if not email:
        raise ValidationError("メールアドレスを入力してください。")

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValidationError("正しいメールアドレスを入力してください。")

    return email


def validate_email_not_used(email, user=None):
    qs = User.objects.filter(email=email)
    if user:
        qs = qs.exclude(pk=user.pk)

    if qs.exists():
        raise ValidationError("このメールアドレスは既に使用されています。")


# ============================
#  パスワード変更フォーム
# ============================
class CustomPasswordChangeForm(PasswordChangeForm):

    def validate_password_rules(self, pw):
        if len(pw) < 10:
            self.add_error('new_password1', "10文字以上必要です。")
        if not any(c.isdigit() for c in pw):
            self.add_error('new_password1', "数字を入れてください。")
        if not any(c.islower() for c in pw):
            self.add_error('new_password1', "小文字を入れてください。")
        if not any(c.isupper() for c in pw):
            self.add_error('new_password1', "大文字を入れてください。")

    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get("new_password1")
        pw2 = cleaned.get("new_password2")

        if pw1 and pw2 and pw1 != pw2:
            self.add_error('new_password2', "パスワードが一致しません。")

        if pw1:
            self.validate_password_rules(pw1)

        return cleaned


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
        name = self.cleaned_data.get("user_name", "")
        return validate_user_name_common(name)

    # --- メールアドレスチェック ---
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            return email

        email = validate_email_common(email)

        validate_email_not_used(email)

        return email

    # --- パスワードチェック ---
    def validate_password_rules(self, pw):
        if len(pw) < 10:
            self.add_error('password', "10文字以上必要です。")
        if not any(c.isdigit() for c in pw):
            self.add_error('password', "数字を入れてください。")
        if not any(c.islower() for c in pw):
            self.add_error('password', "小文字を入れてください。")
        if not any(c.isupper() for c in pw):
            self.add_error('password', "大文字を入れてください。")

        try:
            validate_password(pw)
        except ValidationError as e:
            self.add_error('password', " / ".join(e.messages))

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get("password")
        pw2 = cleaned.get("password2")

        if pw and pw2 and pw != pw2:
            self.add_error('password2', "パスワードが一致しません。")

        if pw:
            self.validate_password_rules(pw)

        return cleaned

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

class CustomPasswordResetForm(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()

        if not email:
            raise ValidationError("メールアドレスを入力してください。")

        if not User.objects.filter(email=email).exists():
            raise ValidationError("このメールアドレスは登録されていません。")

        return email
