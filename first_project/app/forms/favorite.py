from django import forms

class FavoriteItemsForm(forms.Form):
    items = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    def clean_items(self):
        raw = self.cleaned_data.get("items", "")
        if not raw.strip():
            return []
        return [i.strip() for i in raw.split("||") if i.strip()]