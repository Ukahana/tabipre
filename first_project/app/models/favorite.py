from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("ユーザーID")
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
      verbose_name = _("お気に入りリスト")
      verbose_name_plural = _("お気に入りリスト")
    
class FavoriteItem(models.Model):
    favorite = models.ForeignKey(
        Favorite,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("お気に入りリストID")
    )

    item_name = models.CharField(
        max_length=128,
        verbose_name=_("項目名")
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
      verbose_name = _("お気に入りリストの項目")
      verbose_name_plural = _("お気に入りリストの項目")
   