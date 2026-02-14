document.addEventListener("DOMContentLoaded", function () {
    const modalEl = document.getElementById("editItemModal");
    if (!modalEl) return;

    const modal = new bootstrap.Modal(modalEl);

    // ① 編集ボタンを押してモーダルを開く
    modalEl.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        if (!button) return;

        const itemId = button.dataset.itemId;
        const itemName = button.dataset.itemName;

        document.getElementById("editItemId").value = itemId;
        document.getElementById("editItemInput").value = itemName;

    });

    // ② モーダルが開いたら入力欄にフォーカス
    modalEl.addEventListener("shown.bs.modal", function () {
        const input = document.getElementById("editItemInput");
        const len = input.value.length;
        input.focus();
        input.setSelectionRange(len, len);
    });

    // ③ エラー時に自動でモーダルを開く
    if (modalEl.dataset.open === "1") {
        const itemId = modalEl.dataset.itemId;
        const itemName = modalEl.dataset.itemName;

        document.getElementById("editItemId").value = itemId;
        document.getElementById("editItemInput").value = itemName;

        modal.show();
    }
});