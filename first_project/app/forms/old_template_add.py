from django import forms

class OldCategoryItemForm(forms.Form):
    category_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "例：衣類"}),
        error_messages={
            "required": "分類名を入力してください。",
            "max_length": "分類名は50文字以内で入力してください。",
        }
    )

    item_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "未入力でも追加できます"}),
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
        widget=forms.HiddenInput()
    )

    def clean_item_name(self):
        return (self.cleaned_data.get("item_name") or "").strip()

    def clean_favorite_flag(self):
        value = self.cleaned_data.get("favorite_flag")
        return 1 if str(value) == "1" else 0