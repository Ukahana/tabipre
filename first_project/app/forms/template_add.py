from django import forms
import unicodedata
from ..models.template import TravelCategory, TravelItem


def normalize(text):
    if not text:
        return ""
    return unicodedata.normalize("NFKC", text).strip()


class CategoryItemForm(forms.Form):
    category_name = forms.CharField(
        max_length=50,
        required=True,
        error_messages={
            "required": "分類名は必須です。",
            "max_length": "分類名は50文字以内で入力してください。",
        }
    )

    item_name = forms.CharField(
        max_length=50,
        required=False,
        error_messages={
            "max_length": "項目名は50文字以内で入力してください。",
        }
    )

    category_color = forms.IntegerField(
        required=True,
        error_messages={
            "required": "カラーは必須です。",
            "invalid": "カラー選択が不正です。",
        }
    )

    favorite_flag = forms.TypedChoiceField(
        choices=[("0", 0), ("1", 1)],
        coerce=int,
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.template = kwargs.pop("template", None)
        super().__init__(*args, **kwargs)

    def clean_category_name(self):
        return normalize(self.cleaned_data["category_name"])

    def clean_item_name(self):
        return normalize(self.cleaned_data.get("item_name", ""))

    def clean(self):
        cleaned_data = super().clean()
        category_name = cleaned_data.get("category_name")
        item_name = cleaned_data.get("item_name")

        if not item_name:
            return cleaned_data

        # 分類を取得
        category = TravelCategory.objects.filter(
            template=self.template,
            category_name=category_name
        ).first()

        if category:
            # TravelItem で重複チェック
            if TravelItem.objects.filter(
                travel_category=category,
                item_name=item_name
            ).exists():
                self.add_error("item_name", "同じ分類内に同じ項目名が既に存在します。")

        return cleaned_data