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
    #ここから　コパの履歴コーどを見て修正する
    
    
    
    
    # class ResistForm(forms.ModelForm):
    # password1 = forms.CharField(
    #     label="パスワード",
    #     widget=forms.PasswordInput,
    # )
    # password2 = forms.CharField(
    #     label="パスワード（確認用）",
    #     widget=forms.PasswordInput,
    # )

    # class Meta:
    #     model = User
    #     fields = ['username', 'email']  # 画面に出すのは username, email, password1, password2

    # # パスワード強度チェック
    # def clean_password1(self):
    #     password = self.cleaned_data.get('password1')

    #     # ① 10文字以上
    #     if len(password) < 10:
    #         raise forms.ValidationError("パスワードは10文字以上で入力してください。")

    #     # ② 英字と数字を含む
    #     if not re.search(r'[a-zA-Z]', password) or not re.search(r'[0-9]', password):
    #         raise forms.ValidationError("パスワードには英字と数字を含めてください。")

    #     # ③ 大文字と小文字を含む
    #     if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
    #         raise forms.ValidationError("パスワードには大文字と小文字を含めてください。")

    #     # Django 標準のバリデーション
    #     validate_password(password)

    #     return password

    # # パスワード一致チェック
    # def clean(self):
    #     cleaned_data = super().clean()
    #     p1 = cleaned_data.get("password1")
    #     p2 = cleaned_data.get("password2")

    #     if p1 and p2 and p1 != p2:
    #         self.add_error("password2", "パスワードが一致しません。")

    #     return cleaned_data

    # # 保存処理
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     if commit:
    #         user.save()
    #     return user
