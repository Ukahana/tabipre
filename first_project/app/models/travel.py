from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Transport(models.Model):
    
    # 選択肢 
    # defalteは設定する？
    class TransportType(models.IntegerChoices):
     SHINKANSEN = 0, _("新幹線")
     AIRPLANE   = 1, _("飛行機")
     CAR        = 2, _("車")
     TRAIN      = 3, _("電車")
     BUS        = 4, _("バス")
     OTHER      = 5, _("その他自由記入")

        
    transport_id = models.AutoField(
        primary_key=True,
        verbose_name=_("交通手段ID")
    )
    
    transport_type = models.IntegerField(
    choices=TransportType.choices,
    verbose_name=_("交通手段")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("作成日")
    )
    updated_at = models.DateTimeField(
       auto_now=True,
        verbose_name=_("更新日")
    )

    class Meta:
        verbose_name = _("交通手段")
        verbose_name_plural = _("交通手段")

    def __str__(self):
        return self.get_transport_type_display()

class Travel_info(models.Model):
    # 選択肢
    class StayType(models.IntegerChoices):
        DAY_TRIP = 0, _("日帰り")
        STAY     = 1, _("宿泊")

    class LocationType(models.IntegerChoices):
        DOMESTIC = 0, _("国内")
        OVERSEAS = 1, _("海外")

    class StatusType(models.IntegerChoices):
        NOT_DONE  = 0, _("未")
        COMPLETE  = 1, _("完")
        PROCESSED = 2, _("済") 
        
    # カラムの設定
    travel_info_id = models.AutoField(
        primary_key=True,
        verbose_name=_("旅行情報ID")
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name=_("ユーザーID")
    )
    
    travel_title = models.CharField(
        max_length=100,
        verbose_name=_("旅行タイトル")
    )
    
    start_date = models.DateTimeField(
        verbose_name=_("開始日")
    )
    
    end_date = models.DateTimeField(
        verbose_name=_("終了日")
    )
    
    stay_type = models.IntegerField(
        choices=StayType.choices,
        verbose_name=_("宿泊タイプ")
    )

    location = models.IntegerField(
        choices=LocationType.choices,
        verbose_name=_("場所")
    )

    memo = models.CharField(
        max_length=230,
        blank=True,
        verbose_name=_("メモ")
    )
    
    status = models.IntegerField(
        choices=StatusType.choices,
        default=0,
        verbose_name=_("ステータス")
    )

    # 中間テーブル
    transport = models.ManyToManyField(
        "Transport",
        through="Travelmode",
        verbose_name=_("交通手段")
    )


    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("作成日")
    )
    updated_at = models.DateTimeField(
       auto_now=True,
        verbose_name=_("更新日")
    )
    
    class Meta:
        verbose_name = _("旅行情報")
        verbose_name_plural = _("旅行情報")

  #旅行の管理
    def __str__(self):
       return f"{self.travel_title} ({self.user.username})"

class Travelmode(models.Model):
    travel_info = models.ForeignKey(
        Travel_info,
        on_delete=models.CASCADE,
        verbose_name=_("旅行情報ID")
    )

    transport = models.ForeignKey(
        Transport,
         on_delete=models.CASCADE,
        verbose_name=_("交通手段ID")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("作成日")
    )
    updated_at = models.DateTimeField(
       auto_now=True,
        verbose_name=_("更新日")
    )
    
    class Meta:
      verbose_name = _("旅行の交通手段")
      verbose_name_plural = _("旅行の交通手段")
      unique_together = ('travel_info', 'transport')



