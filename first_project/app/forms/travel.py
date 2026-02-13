from django import forms
from ..models import Travel_info, Transport, Travelmode


# ---------------------------------------------------------
# ★ BaseForm（共通設定）
# ---------------------------------------------------------
class TravelBaseForm(forms.ModelForm):
    class Meta:
        model = Travel_info
        fields = []
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "text"}),
            "end_date": forms.DateInput(attrs={"type": "text"}),
        }
        input_formats = ["%Y.%m.%d", "%Y-%m-%d"]



# ---------------------------------------------------------
# ★ Step1（タイトル・日付・宿泊タイプ）【修正版】
# ---------------------------------------------------------
class TravelStep1Form(TravelBaseForm):
    start_date = forms.DateField(
        input_formats=["%Y.%m.%d", "%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "text"})
    )
    end_date = forms.DateField(
        input_formats=["%Y.%m.%d", "%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "text"})
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

    def clean(self):
        cleaned = super().clean()

        start = cleaned.get("start_date")
        end = cleaned.get("end_date")

        # 日付未入力（Django の required が自動でエラーを出すので追加しない）
        if not start or not end:
            return cleaned

        # 日付逆転
        if end < start:
            self.add_error("end_date", "終了日は開始日より後の日付を選択してください。")

        # 60日超
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
            "memo": forms.Textarea(attrs={"rows": 5, "class": "memo-box"}),
        }

    def __init__(self, *args, **kwargs):
        travel = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        # location の設定
        self.fields["location"].choices = Travel_info.LocationType.choices
        self.fields["location"].required = False   # ★ ここを False に変更

        # 編集時の初期値
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
        
        if cleaned.get("location") == "":
            cleaned["location"] = None

        transports = cleaned.get("transport_types")
        other_text = cleaned.get("transport_other", "").strip()
        location = cleaned.get("location")
        memo = cleaned.get("memo", "")
        
        cleaned["memo"] = memo.strip()

        # 交通手段が 0 個
        if not transports:
            self.add_error("transport_types", "交通手段を1つ以上選択してください。")

        # その他選択時の入力必須
        if transports and any(t.transport_type == Transport.TransportType.OTHER for t in transports):
            if not other_text:
                self.add_error("transport_other", "その他を選択した場合は入力が必要です。")

        # location 未選択
        if location is None:
            self.add_error("location", "場所を選択してください。")

        # memo 文字数
        if len(memo) > 230:
            self.add_error("memo", "メモは230文字以内で入力してください。")

        # その他入力 100 文字超
        if len(other_text) > 100:
            self.add_error("transport_other", "その他の交通手段は100文字以内で入力してください。")

        return cleaned