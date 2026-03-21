function submitCategoryForm(action) {

    const form = document.getElementById('categoryItemForm');
    const flag = document.getElementById("continueFlag");

    if (action === "first") {
        flag.value = "0";   // 最初のバリデーション
        form.submit();
        return;
    }

    if (action === "continue") {
        flag.value = "1";   // はい（保存済み → add_category_item に戻る）
        form.submit();
        return;
    }

    // cancel はもう使わない（画面遷移で処理する）
}