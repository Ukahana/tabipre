from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date
from ..models import Link


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ["permission_type", "expiration_type", "expiration_date"]
        widgets = {
            "permission_type": forms.RadioSelect(attrs={"class": "permission-radio"}),
            "expiration_type": forms.RadioSelect(),
            "expiration_date": forms.TextInput(
                attrs={
                    "type": "text",
                    "autocomplete": "off",
                    "placeholder": "例: 2026-3-1 , 2026/3/1 , 2026.3.1",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["expiration_date"].required = False

    # ▼ 年あり形式のみ許可
    def clean_expiration_date(self):
        value = self.cleaned_data.get("expiration_date")
        if not value:
            return value

        if isinstance(value, date):
            return value

        normalized = (
            str(value)
            .strip()
            .replace(" ", "")
            .replace("/", "-")
            .replace(".", "-")
        )

        parts = normalized.split("-")

        try:
            # ★ 年なし（2/1 など）は不許可
            if len(parts) != 3:
                raise ValueError

            year, month, day = parts

            month = month.zfill(2)
            day = day.zfill(2)

            parsed = date(int(year), int(month), int(day))
            return parsed

        except Exception:
            raise ValidationError("正しい日付を入力してください（例: 2026-3-1）")

    # ▼ expiration_type=2 のときだけ日付必須
    def clean(self):
        cleaned = super().clean()
        exp_type = cleaned.get("expiration_type")
        exp_date = cleaned.get("expiration_date")

        if exp_type == 2:
            if not exp_date:
                self.add_error("expiration_date", "日付を入力してください。")
            elif exp_date < timezone.now().date():
                self.add_error("expiration_date", "過去の日付は指定できません。")
        else:
            if "expiration_date" in self._errors:
                del self._errors["expiration_date"]

        return cleaned