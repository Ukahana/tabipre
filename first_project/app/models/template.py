from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .travel import Travel_info

class Template(models.Model):
    # 選択肢
    class SourceType(models.IntegerChoices):
        FROM_TRAVEL   = 0, _("旅行情報より作成")
        FROM_TEMPLATE = 1, _("既存テンプレートを反映")

    # カラムの設定
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("ユーザーID")
    )

    travel_info = models.ForeignKey(
        Travel_info,
        on_delete=models.CASCADE,
        verbose_name=_("旅行情報ID")
    )
    
    source_type = models.IntegerField(
        choices=SourceType.choices,
        verbose_name=_("生成タイプ")
    )

    # ERだとint,FKに戻すか再検討
    template_source = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("テンプレート参照元"),
        related_name="derived_templates"
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
      verbose_name = _("テンプレート")
      
    def __str__(self):
     return f"Template {self.id} ({self.user})"


class TravelCategory(models.Model):
    # 選択肢
    class TravelType(models.IntegerChoices):
        AUTO  = 0, _("初期作成")
        CUSTOM = 1, _("ユーザー追加")

    class CategoryColor(models.IntegerChoices):
        PINK       = 0, "#e91e63ff"
        LIGHT_PINK = 1, "#ffb7b2fe"
        ORANGE     = 2, "#f57c00ff"
        GREEN      = 3, "#388e3cff"
        CYAN       = 4, "#0097a7ff"
        BLUE       = 5, "#303f9ffe"
        BROWN      = 6, "#795548ff"
        PURPLE     = 7, "#7b1fa2ff"

    # カラムの設定
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        verbose_name=_("テンプレートID")
    )
    
    category_name = models.CharField(
        max_length=50,
        verbose_name=_("分類名")
    )

    travel_type = models.IntegerField(
        choices=TravelType.choices,
        verbose_name=_("分類タイプ")
    )
    
    category_color = models.IntegerField(
        choices=CategoryColor.choices,
        verbose_name=_("分類カラー")
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
      verbose_name = _("旅行の分類")
      
    def __str__(self):  
     return f"Category {self.category_name} (Template {self.template_id})"

class TravelItem(models.Model):
    # 選択肢
    class ItemChecked(models.IntegerChoices):
        NO  = 0, _("NO")
        YES = 1, _("YES")


    # カラムの設定
    travel_category = models.ForeignKey(
        TravelCategory,
        on_delete=models.CASCADE,
        verbose_name=_("旅行の分類ID")
    )
    
    item_name = models.CharField(
        max_length=128,
        verbose_name=_("項目名")
    )

    item_checked = models.IntegerField(
        choices=ItemChecked.choices,
        verbose_name=_("チェック済み項目")
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
      verbose_name = _("旅行の項目")
      
    def __str__(self):
      return f"{self.item_name} ({self.travel_category})"
