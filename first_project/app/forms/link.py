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
            "expiration_date": forms.DateInput(
                attrs={
                    "type": "date",   # カレンダー入力
                    "autocomplete": "off",
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
            (Link.ExpirationType.ONE_MONTH, "1か月間有効："),
            (Link.ExpirationType.AFTER_TRIP, "旅行終了日の翌日まで："),
            (Link.ExpirationType.USER_INPUT, "日付を指定する"),
        ]