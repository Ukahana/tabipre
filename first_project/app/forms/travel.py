from django import forms
from ..models import (Travel_info,Transport,Template)

STAY_CHOICES = [
    ('daytrip', '日帰り'),
    ('overnight', '宿泊'),
]

class TravelStep1Form(forms.ModelForm):
    stay_type = forms.ChoiceField(
        choices=STAY_CHOICES,
        widget=forms.RadioSelect,
        label="宿泊タイプ",
        required=True
    )

    class Meta:
        model = Travel_info
        fields = ['travel_title', 'start_date', 'end_date', 'stay_type']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start_date")
        end = cleaned.get("end_date")

        if not cleaned.get("travel_title"):
            self.add_error("travel_title", "旅行タイトルを入力してください。")
        if not start:
            self.add_error("start_date", "開始日を入力してください。")
        if not end:
            self.add_error("end_date", "終了日を入力してください。")
        if start and end and start > end:
            self.add_error("end_date", "終了日は開始日以降の日付を指定してください。")

        return cleaned


        
class TravelStep2Form(forms.Form):
    # 国内 / 海外
    location = forms.ChoiceField(
        choices=Travel_info.LocationType.choices,
        widget=forms.RadioSelect,
        label="場所"
    )

    # 交通手段（チェックボックス）
    transport = forms.ModelMultipleChoiceField(
        queryset=Transport.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="交通手段",
        required=False
    )

    # その他自由記入
    transport_other = forms.CharField(
        max_length=100,
        required=False,
        label="その他（自由記入）"
    )

    # メモ
    memo = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
        label="メモ"
    )
    def clean(self):
        cleaned = super().clean()
        transport = cleaned.get("transport")
        other = cleaned.get("transport_other")

        if not transport and not other:
            self.add_error("transport", "交通手段を選択するか、その他を入力してください。")

        return cleaned
   

class TravelEditForm(forms.ModelForm):
    class Meta:
        model = Travel_info
        fields = ["travel_title", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

class TemplateEditForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['template_source']
        # かえるかも↑
