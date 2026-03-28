document.addEventListener("DOMContentLoaded", function () {
    const modalEl = document.getElementById("editItemModal");
    if (!modalEl) return;

    const modal = new bootstrap.Modal(modalEl);

    modalEl.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        if (!button) return;

        const itemId = button.dataset.itemId;
        const itemName = button.dataset.itemName;

        // 編集対象IDと名前をセット
        document.getElementById("editItemId").value = itemId;
        document.getElementById("editItemInput").value = itemName;

        // 削除ボタンに情報をセット
        const deleteBtn = modalEl.querySelector('.delete-item-btn');
        deleteBtn.dataset.id = itemId;
        deleteBtn.dataset.name = itemName;
    });

    // モーダルが開いたら入力欄にフォーカス
    modalEl.addEventListener("shown.bs.modal", function () {
        const input = document.getElementById("editItemInput");
        const len = input.value.length;
        input.focus();
        input.setSelectionRange(len, len);
    });

    // 削除ボタン → 削除モーダルを開く
    modalEl.addEventListener("click", function (e) {
        const btn = e.target.closest(".delete-item-btn");
        if (!btn) return;

        e.preventDefault();

        const itemId = btn.dataset.id;
        const itemName = btn.dataset.name;

        document.getElementById("deleteMessage").textContent =
            `項目「${itemName}」を削除しますか？`;

        // 削除 hidden input にセット
        document.getElementById("deleteItemInput").value = itemId;

        // 編集モーダルを閉じて削除モーダルを開く
        modal.hide();

        modalEl.addEventListener("hidden.bs.modal", function handler() {
            modalEl.removeEventListener("hidden.bs.modal", handler);

            const deleteModalEl = document.getElementById("confirmDeleteModal");
            const deleteModal = new bootstrap.Modal(deleteModalEl);
            deleteModal.show();
        });
    });
});