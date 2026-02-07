document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("editItemModal");
    if (!modal) return;

    // モーダルが開く直前に発火
    modal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;

        // ★ あなたの data 属性に合わせる
        const itemId = button.dataset.id;
        const itemName = button.dataset.name;

        // hidden に ID をセット
        document.getElementById("editItemId").value = itemId;

        // 入力欄に名前をセット
        const input = document.getElementById("editItemInput");
        input.value = itemName;
    });

    // モーダルが完全に開いた後にカーソルを末尾へ
    modal.addEventListener("shown.bs.modal", function () {
        const input = document.getElementById("editItemInput");
        const len = input.value.length;

        input.focus();
        input.setSelectionRange(len, len);
    });
});