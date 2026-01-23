from ...models.template import Template, TravelCategory, TravelItem
from ...models.travel import Travel_info, Transport

INITIAL_ITEMS = {
    "共通": [
        "宿泊・交通の予約内容を確認",
        "天気・現地情報の確認",
        "服（何泊分）",
        "コスメ・スキンケア",
        "充電器類",
        "常備薬",
    ],
    "国内": ["現地の交通手段を準備", "観光地の営業時間を確認"],
    "海外": ["パスポート", "外貨両替", "通信手段（SIM/Wi-Fi）の準備"],
    "飛行機": ["航空券予約", "空港アクセス確認", "荷物制限確認"],
    "新幹線": ["チケットの予約", "乗車時間・乗り継ぎの確認"],
    "車": ["ガソリンを入れる", "ETCの確認", "移動ルート・駐車場の確認"],
    "バス": ["乗車場所・乗り継ぎの確認"],
    "電車": ["ICカードの準備", "乗り継ぎの確認"],
    "その他": ["ルート・時間を確認", "予約が必要か確認"],
}


def template_source(travel, user):

    # Template 作成
    template = Template.objects.create(
        user=user,
        travel_info=travel,
        source_type=Template.SourceType.FROM_TRAVEL
    )

    # 泊数を計算（例：1/1〜1/3 → 2泊）
    nights = (travel.end_date - travel.start_date).days

    # 日帰りは「1日分」にする（UX的に自然）
    if nights <= 0:
        clothes_label = "服（1日分）"
    else:
        clothes_label = f"服（{nights}泊分）"

    # 分類リスト
    categories = []

    # 共通
    categories.append("共通")

    # 国内/海外
    if travel.location == Travel_info.LocationType.DOMESTIC:
        categories.append("国内")
    else:
        categories.append("海外")

    # 交通手段
    for tm in travel.travelmode_set.all():
        t = tm.transport.transport_type

        if t == Transport.TransportType.AIRPLANE:
            categories.append("飛行機")
        elif t == Transport.TransportType.SHINKANSEN:
            categories.append("新幹線")
        elif t == Transport.TransportType.CAR:
            categories.append("車")
        elif t == Transport.TransportType.BUS:
            categories.append("バス")
        elif t == Transport.TransportType.TRAIN:
            categories.append("電車")
        elif t == Transport.TransportType.OTHER:
            if tm.custom_transport_text.strip():
                categories.append(tm.custom_transport_text.strip())
            else:
                categories.append("その他")

    CATEGORY_COLOR_MAP = {
        "共通": TravelCategory.CategoryColor.BLUE,
        "国内": TravelCategory.CategoryColor.GREEN,
        "海外": TravelCategory.CategoryColor.GREEN,
        "飛行機": TravelCategory.CategoryColor.CYAN,
        "新幹線": TravelCategory.CategoryColor.PINK,
        "車": TravelCategory.CategoryColor.ORANGE,
        "バス": TravelCategory.CategoryColor.BROWN,
        "電車": TravelCategory.CategoryColor.LIGHT_PINK,
        "その他": TravelCategory.CategoryColor.PURPLE,
    }

    DEFAULT_OTHER_COLOR = TravelCategory.CategoryColor.PURPLE

    # TravelCategory & TravelItem 作成
    for cat in categories:
        color = CATEGORY_COLOR_MAP.get(cat, DEFAULT_OTHER_COLOR)

        category = TravelCategory.objects.create(
            template=template,
            category_name=cat,
            travel_type=TravelCategory.TravelType.AUTO,
            category_color=color
        )

        key = cat if cat in INITIAL_ITEMS else "その他"

        for item in INITIAL_ITEMS.get(key, []):

            # ★ 服（何泊分）だけ泊数に応じて置き換える
            if item == "服（何泊分）":
                item_name = clothes_label
            else:
                item_name = item

            TravelItem.objects.create(
                travel_category=category,
                item_name=item_name,
                item_checked=TravelItem.ItemChecked.NO
            )

    return template