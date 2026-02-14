window.submitCategoryForm = function(action) {

    const form = document.getElementById("categoryItemForm");
    const flag = document.getElementById("continueFlag");

    if (action === "first") {
        // まずバリデーションのために送信する（モーダルは開かない）
        flag.value = "0";
        form.submit();
        return;
    }

    if (action === "continue") {
        // はい → 続けて追加（GET遷移）
        const url = form.getAttribute("action");  // /category_item_add/<id>/
        window.location.href = url;
        return;
    }

    if (action === "cancel") {
        // いいえ → 編集画面へ戻る（GET遷移）
        const editUrl = document.getElementById("continueModal").dataset.editUrl;
        window.location.href = editUrl;
        return;
    }
};