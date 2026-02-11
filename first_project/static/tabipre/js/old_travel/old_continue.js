window.submitCategoryForm = function(action) {

    const form = document.getElementById("categoryItemForm");
    const flag = document.getElementById("continueFlag");

    if (action === "first") {
        // ここでは送信しない
        flag.value = "0";

        // モーダルを開くだけ
        const modalEl = document.getElementById("continueModal");
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
        return;  // ← これが超重要
    }

    if (action === "continue") {
        flag.value = "1";   // はい（保存して続ける）
    } else if (action === "cancel") {
        flag.value = "2";   // いいえ（保存して戻る）
    }

    form.submit();
};