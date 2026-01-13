from django import forms
from ..models import Link

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = [
            "permission_type",
            "expiration_type",
            "expiration_date",
        ]
        widgets = {
            "permission_type": forms.RadioSelect,
            "expiration_type": forms.RadioSelect,
            "expiration_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["expiration_date"].required = False

    def clean(self):
        cleaned_data = super().clean()
        expiration_type = cleaned_data.get("expiration_type")
        expiration_date = cleaned_data.get("expiration_date")

        # ユーザー入力のときだけ日付必須
        if expiration_type == Link.ExpirationType.USER_INPUT and not expiration_date:
            self.add_error("expiration_date", "ユーザー入力の場合、有効期限を入力してください。")

        return cleaned_data