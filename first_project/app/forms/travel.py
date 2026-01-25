from django import forms
from ..models import Travel_info, Transport, Travelmode


# ★ 共通の BaseForm（Travel_info の共通設定）
class TravelBaseForm(forms.ModelForm):
    class Meta:
        model = Travel_info
        fields = [] 
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

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get("travel_title", "").strip()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        # タイトル空白チェック
        if not title:
            self.add_error("travel_title", "旅行タイトルを入力してください。")

        # 日付未入力
        if not start or not end:
            self.add_error("start_date", "開始日と終了日を入力してください。")
            return cleaned_data

        # 日付逆転
        if end < start:
            self.add_error("end_date", "終了日は開始日より後の日付を選択してください。")

        # 旅行期間 60 日超
        if (end - start).days > 60:
            self.add_error("end_date", "旅行期間が長すぎます。60日以内にしてください。")

        return cleaned_data



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
        widget=forms.TextInput(attrs={
            "class": "transport-other-input",
            "placeholder": "その他の交通手段を入力"
        })
    )

    class Meta(TravelBaseForm.Meta):
        fields = ["location", "memo"]
        widgets = {
            "location": forms.RadioSelect(),
            "memo": forms.Textarea(attrs={
                "rows": 5,
                "class": "memo-box",
            }),
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
        cleaned_data = super().clean()

        transports = cleaned_data.get("transport_types")
        other_text = cleaned_data.get("transport_other", "").strip()
        location = cleaned_data.get("location")
        memo = cleaned_data.get("memo", "")

        # 交通手段が 0 個
        if not transports or len(transports) == 0:
            self.add_error("transport_types", "交通手段を1つ以上選択してください。")

        # その他選択時の入力必須
        if transports and any(
            t.transport_type == Transport.TransportType.OTHER
            for t in transports
        ):
            if not other_text:
                self.add_error("transport_other", "その他を選択した場合は入力が必要です。")

        # location 未選択
        if location is None:
            self.add_error("location", "場所を選択してください。")

        # memo の文字数チェック（230 文字制限）
        if len(memo) > 230:
            self.add_error("memo", "メモは230文字以内で入力してください。")

        # その他入力 100 文字超
        if len(other_text) > 100:
            self.add_error("transport_other", "その他の交通手段は100文字以内で入力してください。")

        return cleaned_data