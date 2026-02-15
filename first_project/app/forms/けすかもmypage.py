from django import forms
from django.core.exceptions import ValidationError
from app.models import User

# アカウント名変更
class UserNameChangeForm(forms.Form):
    user_name = forms.CharField(
        label="名前 / ニックネーム",
        max_length=30,
        required=True,
        error_messages={
            'required': '名前 / ニックネームを入力してください。',
            'max_length': '30文字以内で入力してください。',
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )


# メールアドレス変更
class EmailChangeForm(forms.Form):
    current_email = forms.EmailField(
        label="現在のメールアドレス",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'oninput': 'this.value = this.value.toLowerCase();'
        }),
        error_messages={
            'required': '現在のメールアドレスを入力してください。',
            'invalid': '正しいメールアドレスを入力してください。',
        }
    )

    new_email = forms.EmailField(
        label="新しいメールアドレス",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'oninput': 'this.value = this.value.toLowerCase();'
        }),
        error_messages={
            'required': '新しいメールアドレスを入力してください。',
            'invalid': '正しいメールアドレスを入力してください。',
        }
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    # 現在のメールアドレスチェック
    def clean_current_email(self):
        current = self.cleaned_data.get("current_email", "").strip().lower()
        stored = (self.user.email or "").strip().lower()


        if current != stored:
            raise ValidationError("現在のメールアドレスが正しくありません。")

        return current

    # 新しいメールアドレスチェック
    def clean_new_email(self):
        new = self.cleaned_data.get("new_email", "").strip().lower()

        # ① 現在と同じ → エラー
        if new == self.user.email:
            raise ValidationError("現在のメールアドレスと同じです。変更はありません。")

        # ② 既に他ユーザーが使用している → エラー
        if User.objects.filter(email=new).exists():
            raise ValidationError("このメールアドレスは既に使用されています。")

        return new