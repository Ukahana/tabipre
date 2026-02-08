document.addEventListener("DOMContentLoaded", function () {
    const modalEl = document.getElementById("editItemModal");
    if (!modalEl) return;

    const modal = new bootstrap.Modal(modalEl);

    // ① 通常の「編集ボタンを押して開く」処理
    modalEl.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        if (!button) return;  // ★ エラー時は relatedTarget が null

        const itemId = button.dataset.itemId;
        const itemName = button.dataset.itemName;

        document.getElementById("editItemId").value = itemId;
        document.getElementById("editItemInput").value = itemName;

        const form = document.getElementById("editItemForm");
        form.action = `/item/edit/${itemId}/`;
    });

    // ② モーダルが開いたら入力欄にフォーカス
    modalEl.addEventListener("shown.bs.modal", function () {
        const input = document.getElementById("editItemInput");
        const len = input.value.length;
        input.focus();
        input.setSelectionRange(len, len);
    });

    // ③ ★ エラー時に自動でモーダルを開く（＋値セット）
    if (modalEl.dataset.open === "1") {
        const itemId = modalEl.dataset.itemId;  // ← Django から渡す
        const itemName = modalEl.dataset.itemName;

        // 値をセット
        document.getElementById("editItemId").value = itemId;
        document.getElementById("editItemInput").value = itemName;

        // form.action をセット
        const form = document.getElementById("editItemForm");
        form.action = `/item/edit/${itemId}/`;

        modal.show();
    }
});