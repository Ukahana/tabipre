from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .template import Template

class Link(models.Model):
    # 選択肢
    class PermissionType(models.IntegerChoices):
        READ_ONLY    = 0, _("閲覧のみ")
        EDITABLE     = 1, _("編集可能")

    class ExpirationType(models.IntegerChoices):
        ONE_MONTH = 0, _("1か月間")
        AFTER_TRIP = 1, _("旅行終了日翌日")
        USER_INPUT = 2, _("ユーザー入力")


    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        verbose_name=_("テンプレートID")
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("ユーザーID")
    )

    share_token = models.CharField(
        max_length=64,
        verbose_name=_("共有トークン")
    )

    permission_type = models.IntegerField(
        choices=PermissionType.choices,
        default=PermissionType.READ_ONLY,
        verbose_name=_("編集権限")
    )
    expiration_type = models.IntegerField(
        choices=ExpirationType.choices,
        default=ExpirationType.ONE_MONTH,
        verbose_name=_("有効期限タイプ")
    )

    expiration_date = models.DateField(
         verbose_name=_("有効期限")
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
      verbose_name = _("共有リンク")
      verbose_name_plural = _("共有リンク")
