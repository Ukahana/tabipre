from django import forms
from ..models import Travel_info, Transport, Travelmode


# ---------------------------------------------------------
# ★ BaseForm（共通設定）
# ---------------------------------------------------------
class TravelBaseForm(forms.ModelForm):
    class Meta:
        model = Travel_info
        fields = []
        # ★ Base には日付ウィジェットを書かない（Step1 で上書きするため）
        input_formats = ["%Y.%m.%d", "%Y-%m-%d"]


# ---------------------------------------------------------
# ★ Step1（タイトル・日付・宿泊タイプ）
# ---------------------------------------------------------
from django import forms

class TravelStep1Form(TravelBaseForm):
    start_date = forms.DateField(
        input_formats=["%Y.%m.%d", "%Y-%m-%d"],
        widget=forms.TextInput(
            attrs={
                "class": "date-input",
                "autocomplete": "off",
            }
        )
    )

    end_date = forms.DateField(
        input_formats=["%Y.%m.%d", "%Y-%m-%d"],
            widget=forms.TextInput(
              attrs={
                    "class": "date-input",
                    "autocomplete": "off",
                }
        )
    )
    stay_type = forms.TypedChoiceField(
        choices=Travel_info.StayType.choices,
        coerce=int,
        widget=forms.RadioSelect,
        label="宿泊タイプ",
        required=True,
    )

    class Meta(TravelBaseForm.Meta):
        fields = ["travel_title", "start_date", "end_date", "stay_type"]
        widgets = {
            "travel_title": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned = super().clean()

        start = cleaned.get("start_date")
        end = cleaned.get("end_date")

        if not start or not end:
            return cleaned

        if end < start:
            self.add_error("end_date", "終了日は開始日より後の日付を選択してください。")

        if (end - start).days > 60:
            self.add_error("end_date", "旅行期間が長すぎます。60日以内にしてください。")

        return cleaned

# ---------------------------------------------------------
# ★ Step2（交通手段・その他・場所・メモ）
# ---------------------------------------------------------
class TravelStep2Form(TravelBaseForm):
    transport_types = forms.ModelMultipleChoiceField(
        queryset=Transport.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="交通手段",
    )

    transport_other = forms.CharField(
        max_length=100,
        required=False,
        label="その他の交通手段",
        widget=forms.TextInput(attrs={
            "class": "transport-other-input",
            "placeholder": "交通手段を入力"
        })
    )

    class Meta(TravelBaseForm.Meta):
        fields = ["location", "memo"]
        widgets = {
            "location": forms.RadioSelect(),
            "memo": forms.Textarea(attrs={"rows": 5, "class": "memo-box"}),
        }

    def __init__(self, *args, **kwargs):
        travel = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        self.fields["location"].choices = Travel_info.LocationType.choices
        self.fields["location"].required = True

        if travel:
            self.fields["transport_types"].initial = travel.transport.all()

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

    def clean(self):
        cleaned = super().clean()
        
        transports = cleaned.get("transport_types")
        other_text = cleaned.get("transport_other", "").strip()
        location = cleaned.get("location")
        memo = cleaned.get("memo", "")

        cleaned["memo"] = memo.strip()

        if transports and any(t.transport_type == Transport.TransportType.OTHER for t in transports):
            if not other_text:
                self.add_error("transport_other", "その他を選択した場合は入力が必要です。")

        if len(memo) > 230:
            self.add_error("memo", "メモは230文字以内で入力してください。")

        if len(other_text) > 100:
            self.add_error("transport_other", "その他の交通手段は100文字以内で入力してください。")

        return cleaned