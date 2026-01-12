from django import forms
from ..models import (Travel_info,Transport,Template,Travelmode)

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


class TravelStep2Form(forms.ModelForm):
    transport_types = forms.ModelMultipleChoiceField(
        queryset=Transport.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    transport_other = forms.CharField(
        max_length=100,
        required=False,
    )

    class Meta:
        model = Travel_info
        fields = ["location", "memo"]
        widgets = {
            "location": forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        travel = kwargs.get("instance")
        super().__init__(*args, **kwargs)
        # ★ 空の選択肢を作らせない
        self.fields["location"].required = True
        self.fields["location"].choices = [
        c for c in self.fields["location"].choices if c[0] != ""
        ]
        
        self.fields["location"].choices = Travel_info.LocationType.choices

        if travel:
            # transport の初期値
            self.fields["transport_types"].initial = travel.transport.all()

            # other の初期値
            other_transport = Transport.objects.get(
                transport_type=Transport.TransportType.OTHER
            )
            other_mode = Travelmode.objects.filter(
                travel_info=travel,
                transport=other_transport
            ).first()

            self.fields["transport_other"].initial = (
                other_mode.custom_transport_text if other_mode else ""
            )