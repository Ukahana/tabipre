from django import forms
from ..models.template import TravelCategory, TravelItem


class OldCategoryItemForm(forms.Form):
    category_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "例：衣類",
            "list": "categorySuggestions",
            "autocomplete": "off",
        }),
        error_messages={
            "required": "分類名を入力してください。",
            "max_length": "分類名は50文字以内で入力してください。",
        }
    )

    item_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "未入力でも追加できます",
            "id": "itemNameInput",
            "autocomplete": "off",
        }),
        error_messages={
            "max_length": "項目名は50文字以内で入力してください。",
        }
    )

    category_color = forms.CharField(
        required=True,
        widget=forms.HiddenInput(),
        error_messages={
            "required": "分類の色を選択してください。",
        }
    )

    favorite_flag = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(attrs={"id": "favoriteValue"})
    )

    def __init__(self, *args, **kwargs):
        self.template = kwargs.pop("template", None)
        super().__init__(*args, **kwargs)

    def clean_item_name(self):
        # 空白だけの場合は空文字にする
        return (self.cleaned_data.get("item_name") or "").strip()

    def clean_favorite_flag(self):
        value = self.cleaned_data.get("favorite_flag")
        return 1 if str(value) == "1" else 0

    def clean(self):
        cleaned_data = super().clean()

        category_name = cleaned_data.get("category_name")
        item_name = cleaned_data.get("item_name")

        if not item_name:
            return cleaned_data

        if self.template and category_name:
            try:
                category = TravelCategory.objects.get(
                    template=self.template,
                    category_name=category_name
                )

                if TravelItem.objects.filter(
                    travel_category=category,
                    item_name=item_name
                ).exists():
                    self.add_error("item_name", "この分類には同じ項目がすでに存在します。")

            except TravelCategory.DoesNotExist:
                pass

        return cleaned_data