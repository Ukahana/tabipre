from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, date
from ..models import Link


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ["permission_type", "expiration_type", "expiration_date"]
        widgets = {
            "permission_type": forms.RadioSelect(attrs={"class": "permission-radio"}),
            "expiration_type": forms.RadioSelect(),
            "expiration_date": forms.DateInput(
                attrs={
                    "type": "text",
                    "autocomplete": "off",
                    "placeholder": "例: 2026-02-27 または 2/5",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["expiration_date"].required = False

   
        self.fields["permission_type"].choices = [
            (Link.PermissionType.READ_ONLY, "閲覧のみ：他の人は見るだけで変更できません。"),
            (Link.PermissionType.EDITABLE, "編集可能：他の人も内容を変更できます。"),
        ]

        self.fields["expiration_type"].choices = [
            (0, "1か月間有効："),
            (1, "旅行終了日の翌日まで："),
            (2, "日付を指定する"),
        ]

    def clean_expiration_date(self):
        value = self.cleaned_data.get("expiration_date")
        if not value:
            return value

        if isinstance(value, date):
            return value

        normalized = (
            str(value).strip()
            .replace(" ", "")
            .replace("/", "-")
            .replace(".", "-")
        )

        parts = normalized.split("-")

        try:
            if len(parts) == 3:
                return datetime.strptime(normalized, "%Y-%m-%d").date()
            elif len(parts) == 2:
                year = timezone.now().year
                return datetime.strptime(f"{year}-{normalized}", "%Y-%m-%d").date()
        except ValueError:
            pass

        raise ValidationError("正しい日付を入力してください（例: 2/5）")

    def clean(self):
        cleaned = super().clean()
        exp_type = cleaned.get("expiration_type")
        exp_date = cleaned.get("expiration_date")

        if exp_type == 2:
            if not exp_date:
                self.add_error("expiration_date", "日付を入力してください。")
            elif exp_date < timezone.now().date():
                self.add_error("expiration_date", "過去の日付は指定できません。")

        return cleaned