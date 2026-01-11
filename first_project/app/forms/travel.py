from django import forms
from ..models import (Travel_info,Transport,Template)

STAY_CHOICES = [
    (0, '日帰り'),
    (1, '宿泊'),
]

class TravelStep1Form(forms.ModelForm):
    stay_type = forms.TypedChoiceField(
        choices=Travel_info.StayType.choices, 
        coerce=int,
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

        if start and end and start > end:
            self.add_error("end_date", "終了日は開始日より後の日付を選んでください。")

        return cleaned


        
class TravelStep2Form(forms.Form):
    # 国内 / 海外
    location = forms.ChoiceField(
        choices=Travel_info.LocationType.choices,
        widget=forms.RadioSelect,
        label="場所"
    )

    # TransportType をチェックボックスで表示
    transport_types = forms.ModelMultipleChoiceField(
      queryset=Transport.objects.all(),
      widget=forms.CheckboxSelectMultiple,
      label="交通手段（複数選択可）",
      required=False
    )


    # その他自由記入
    transport_other = forms.CharField(
        max_length=100,
        required=False,
        label="その他",
        widget=forms.TextInput(attrs={
            "class": "transport-other-input",
            "placeholder": "その他の交通手段"
        })
    )


    memo = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        required=False,
        label="メモ"
    )

    def clean(self):
      cleaned = super().clean()
      transport_types = cleaned.get("transport_types")
      other = cleaned.get("transport_other")

      # どちらも空ならエラー
      if not transport_types and not other:
        self.add_error("transport_types", "交通手段を選択してください。")

      # その他が入力されているのに OTHER が選ばれていない場合
      if other and transport_types and not transport_types.filter(
          transport_type=Transport.TransportType.OTHER
        ).exists():
        self.add_error("transport_types", "「その他」を入力した場合は、「その他」を選択してください。")

      return cleaned
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["transport_types"].queryset = Transport.objects.all()

   

class TravelEditForm(forms.ModelForm):
    stay_type = forms.TypedChoiceField(
        choices=Travel_info.StayType.choices,
        coerce=int,
        widget=forms.RadioSelect,
        label="宿泊タイプ",
        required=True
    )

    class Meta:
        model = Travel_info
        fields = ["travel_title", "start_date", "end_date", "stay_type"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start_date")
        end = cleaned.get("end_date")

        if start and end and start > end:
            self.add_error("end_date", "終了日は開始日より後の日付を選んでください。")

        return cleaned

class TemplateEditForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['template_source']

