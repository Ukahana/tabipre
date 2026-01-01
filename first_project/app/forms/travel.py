from django import forms
from ..models.travel import (Travel_info,Transport)

class TravelStep1Form(forms.ModelForm):
    class Meta:
        model = Travel_info
        fields = ['travel_title', 'start_date', 'end_date', 'stay_type']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),

        }
        
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
