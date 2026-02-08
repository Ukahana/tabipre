from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from app.models.template import Template, TravelCategory, TravelItem
from app.models.favorite import Favorite, FavoriteItem
from app.forms.old_template_add import OldCategoryItemForm


def category_item_add(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    favorite, _ = Favorite.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = OldCategoryItemForm(request.POST)

        # ★ form.is_valid() は「型チェック」だけに使う
        if form.is_valid():
            category_name = form.cleaned_data["category_name"].strip()
            item_name = form.cleaned_data["item_name"].strip()
            color = form.cleaned_data.get("category_color")
            favorite_flag = form.cleaned_data["favorite_flag"]

            # -----------------------------
            # ① 必須チェック（ビュー側で行う）
            # -----------------------------
            if not category_name:
                messages.error(request, "分類名を入力してください。")
                return redirect("app:category_item_add", template_id=template.id)

            # 項目名だけ入力されている → エラー
            if item_name and not category_name:
                messages.error(request, "項目名だけの追加はできません。分類名を入力してください。")
                return redirect("app:category_item_add", template_id=template.id)

            # 色が選択されていない
            if not color:
                messages.error(request, "分類の色を選択してください。")
                return redirect("app:category_item_add", template_id=template.id)

            # -----------------------------
            # ② 分類名の重複チェック
            # -----------------------------
            existing_category = TravelCategory.objects.filter(
                template=template,
                category_name=category_name
            ).first()

            if existing_category:
                category = existing_category
            else:
                category = TravelCategory.objects.create(
                    template=template,
                    category_name=category_name,
                    travel_type=TravelCategory.TravelType.CUSTOM,
                    category_color=color,
                )

            # -----------------------------
            # ③ 項目名がある場合のみチェック
            # -----------------------------
            if item_name:

                if len(item_name) > 50:
                    messages.error(request, "項目名は50文字以内で入力してください。")
                    return redirect("app:category_item_add", template_id=template.id)

                if TravelItem.objects.filter(travel_category=category, item_name=item_name).exists():
                    messages.error(request, "同じ名前の項目がすでに存在します。")
                    return redirect("app:category_item_add", template_id=template.id)

                # 項目追加
                TravelItem.objects.create(
                    travel_category=category,
                    item_name=item_name,
                    item_checked=TravelItem.ItemChecked.NO
                )

                # お気に入り登録
                if favorite_flag == 1:
                    FavoriteItem.objects.get_or_create(
                        favorite=favorite,
                        item_name=item_name
                    )

            # -----------------------------
            # ④ ボタン判定（はい / いいえ）
            # -----------------------------
            action = request.POST.get("action")

            if action == "continue":
                return redirect("app:category_item_add", template_id=template.id)

            if action == "finish":
                return redirect("app:old_template_edit", template_id=template.id)

            # action が無い場合の保険
            return redirect("app:old_template_edit", template_id=template.id)

        else:
            # form が invalid の場合（型エラーなど）
            messages.error(request, "入力内容に誤りがあります。")
            return redirect("app:category_item_add", template_id=template.id)

    else:
        form = OldCategoryItemForm()

    categories = TravelCategory.objects.filter(template=template)

    raw_colors = TravelCategory.CategoryColor.choices
    color_list = [{"value": v, "code": code} for v, code in raw_colors]

    favorite_items = FavoriteItem.objects.filter(favorite=favorite)

    return render(request, "old_travel/add_category_item.html", {
        "form": form,
        "template": template,
        "categories": categories,
        "color_list": color_list,
        "favorite_items": favorite_items,
    })