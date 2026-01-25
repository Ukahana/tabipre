from django import forms
from app.models.template import TravelCategory


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

    favorite_flag = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.template = kwargs.pop("template", None)
        super().__init__(*args, **kwargs)

    def clean_category_name(self):
        name = self.cleaned_data["category_name"].strip()

        # 同一テンプレート内での重複チェック
        if self.template:
            if TravelCategory.objects.filter(
                template=self.template,
                category_name=name
            ).exists():
                raise forms.ValidationError("同じ分類名がすでに存在します。")

        return name

    def clean_item_name(self):
        return (self.cleaned_data.get("item_name") or "").strip()