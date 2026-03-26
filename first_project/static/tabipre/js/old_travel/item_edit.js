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

        // 入力欄にセット
        document.getElementById("editItemId").value = itemId;
        document.getElementById("editItemInput").value = itemName;

        // 削除 hidden input にセット
        const deleteInput = document.getElementById("deleteItemId");
        if (deleteInput) {
            deleteInput.value = itemId;
        }

        // 削除ボタンに情報をセット
        const deleteBtn = modalEl.querySelector('.delete-item-btn');
        deleteBtn.dataset.id = itemId;
        deleteBtn.dataset.name = itemName;
    });

    // ② モーダルが開いたら入力欄にフォーカス
    modalEl.addEventListener("shown.bs.modal", function () {
        const input = document.getElementById("editItemInput");
        const len = input.value.length;
        input.focus();
        input.setSelectionRange(len, len);

        const deleteBtn = modalEl.querySelector('.delete-item-btn');
        if (!deleteBtn) return;

        deleteBtn.onclick = function (e) {
            e.preventDefault();

            const itemId = document.getElementById("editItemId").value;
            const itemName = document.getElementById("editItemInput").value;

            // hidden input にセット
            document.getElementById("deleteItemInput").value = itemId;
            document.getElementById("deleteMessage").textContent =
                `項目「${itemName}」を削除しますか？`;

            modal.hide();

            modalEl.addEventListener("hidden.bs.modal", function handler() {
                modalEl.removeEventListener("hidden.bs.modal", handler);

                const deleteModalEl = document.getElementById("confirmDeleteModal");
                const deleteModal = new bootstrap.Modal(deleteModalEl);

                deleteModal.show();
            });
        };
    });

    // ③ エラー時に自動でモーダルを開く
    if (modalEl.dataset.open === "1") {
        modal.show();
    }
});