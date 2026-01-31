from django import forms
import unicodedata


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
        choices=[("0", False), ("1", True)],
        coerce=lambda x: x == "1",
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.template = kwargs.pop("template", None)
        super().__init__(*args, **kwargs)

    def clean_category_name(self):
        return normalize(self.cleaned_data["category_name"])

    def clean_item_name(self):
        return normalize(self.cleaned_data.get("item_name"))