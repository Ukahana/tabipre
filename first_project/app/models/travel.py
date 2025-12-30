from django.db import models
from django.utils.translation import gettext_lazy as _
from .auth import User 

class Travel_info(models.Model):
    # 選択肢
    class StayType(models.IntegerChoices):
        DAY_TRIP = 0, _("日帰り")
        STAY = 1, _("宿泊")

    class LocationType(models.IntegerChoices):
        DOMESTIC = 0, _("国内")
        OVERSEAS = 1, _("海外")

    class StatusType(models.IntegerChoices):
        NOT_DONE = 0, _("未")
        COMPLETE = 1, _("完")
        PROCESSED = 2, _("済") 
        
    # カラムの設定
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=("ユーザーID")
    )
    
    travel_name = models.CharField(
        max_length=100,
        verbose_name=_("旅行名")
    )
    
    start_date = models.models.DateTimeField(
        verbose_name=_("開始日")
    )
    
    end_date = models.models.DateTimeField(
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

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("作成日")
    )
    updated_at = models.DateTimeField(
       auto_now=True,
        verbose_name=_("更新日")
    )
    
#旅行の管理
def __str__(self):
    return f"{self.travel_name} ({self.user.user_name})"