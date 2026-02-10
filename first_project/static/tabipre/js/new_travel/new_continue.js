function submitCategoryForm(action, event) {
    event.preventDefault();

    const form = document.getElementById('categoryItemForm');
    const flag = document.getElementById("continueFlag");

    if (action === "first") {
        flag.value = "0";   // 最初の登録（バリデーション）
    } 
    else if (action === "continue") {
        flag.value = "1";   // モーダルの「はい」（保存）
    } 
    else if (action === "cancel") {
        flag.value = "2";   // ★ モーダルの「いいえ」（戻る）
    }

    form.submit();
}