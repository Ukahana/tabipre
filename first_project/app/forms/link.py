from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, date
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

        # expiration_date は USER_INPUT のときだけ必須にするので False
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

    # ▼ 日付の文字列 → date 変換
    def clean_expiration_date(self):
        date_value = self.cleaned_data.get("expiration_date")

        # 空欄はそのまま
        if not date_value:
            return date_value

        # すでに date 型ならそのまま返す
        if isinstance(date_value, date):
            return date_value

        # 文字列として処理
        date_str = str(date_value).strip()

        normalized = (
            date_str.replace(" ", "")
                    .replace("/", "-")
                    .replace(".", "-")
        )

        try:
            parts = normalized.split("-")

            # YYYY-MM-DD
            if len(parts) == 3:
                parsed = datetime.strptime(normalized, "%Y-%m-%d").date()

            # MM-DD → 年は今年
            elif len(parts) == 2:
                year = timezone.now().year
                parsed = datetime.strptime(f"{year}-{normalized}", "%Y-%m-%d").date()

            else:
                raise ValueError

        except ValueError:
            raise ValidationError("正しい日付を入力してください（例: 2/5）")

        return parsed

    # ▼ expiration_type と expiration_date の整合性チェック
    def clean(self):
        cleaned = super().clean()
        exp_type = cleaned.get("expiration_type")
        exp_date = cleaned.get("expiration_date")

        # USER_INPUT のときだけ日付必須
        if exp_type == 2:
            if not exp_date:
                self.add_error("expiration_date", "日付を入力してください。")
                return cleaned

            # 過去日はNG
            if exp_date < timezone.now().date():
                self.add_error("expiration_date", "過去の日付は指定できません。")

        return cleaned