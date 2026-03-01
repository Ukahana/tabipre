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
                    "readonly": "readonly",
                    "inputmode": "none",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["expiration_date"].required = False

    # ▼ 年なし日付（例：2/1）も許可し、今年の年を補完する
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
            # ▼ 年なし（例：2-1）なら今年を補完
            if len(parts) == 2:
                year = timezone.now().year
                month, day = parts
            elif len(parts) == 3:
                year, month, day = parts
            else:
                raise ValueError

            month = month.zfill(2)
            day = day.zfill(2)

            parsed = date(int(year), int(month), int(day))
            return parsed

        except Exception:
            raise ValidationError("正しい日付を入力してください（例：2026-3-1）")

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
            # 他のタイプでは expiration_date のエラーを消す
            if "expiration_date" in self._errors:
                del self._errors["expiration_date"]

        return cleaned