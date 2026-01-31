from django import forms

class OldCategoryItemForm(forms.Form):
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

    category_color = forms.IntegerField(required=True)

    favorite_flag = forms.BooleanField(required=False)

    def clean_item_name(self):
        return (self.cleaned_data.get("item_name") or "").strip()