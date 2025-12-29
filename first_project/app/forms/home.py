from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='名前', max_length=50)
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)