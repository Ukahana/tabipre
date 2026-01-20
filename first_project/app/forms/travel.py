from django import forms
from ..models import Travel_info, Transport, Travelmode


# ★ 共通の BaseForm（Travel_info の共通設定）
class TravelBaseForm(forms.ModelForm):
    class Meta:
        model = Travel_info
        fields = "__all__"
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


# ★ Step1 用フォーム（タイトル・日付・宿泊タイプ）

class TravelStep1Form(TravelBaseForm):
    stay_type = forms.TypedChoiceField(
        choices=Travel_info.StayType.choices,
        coerce=int,
        widget=forms.RadioSelect,
        label="宿泊タイプ",
        required=True,
    )

    class Meta(TravelBaseForm.Meta):
        fields = ["travel_title", "start_date", "end_date", "stay_type"]



# ★ Step2 用フォーム（交通手段・その他・場所・メモ）

class TravelStep2Form(TravelBaseForm):
    transport_types = forms.ModelMultipleChoiceField(
        queryset=Transport.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="交通手段",
    )

    transport_other = forms.CharField(
        max_length=100,
        required=False,
        label="その他の交通手段",
    )

    class Meta(TravelBaseForm.Meta):
        fields = ["location", "memo"]
        widgets = {
            "location": forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        travel = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        # location の選択肢を明示的にセット（空選択肢を排除）
        self.fields["location"].choices = Travel_info.LocationType.choices
        self.fields["location"].required = True

        if travel:
            # transport の初期値
            self.fields["transport_types"].initial = travel.transport.all()

            # OTHER の初期値
            other_transport = Transport.objects.filter(
                transport_type=Transport.TransportType.OTHER
            ).first()

            if other_transport:
                other_mode = Travelmode.objects.filter(
                    travel_info=travel,
                    transport=other_transport,
                ).first()

                self.fields["transport_other"].initial = (
                    other_mode.custom_transport_text if other_mode else ""
                )