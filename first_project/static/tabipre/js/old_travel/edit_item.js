// 編集モーダルに値をセットする
document.addEventListener("DOMContentLoaded", function () {
    const editModal = document.getElementById("editItemModal");

    if (!editModal) return;

    editModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;

        const itemId = button.getAttribute("data-item-id");
        const itemName = button.getAttribute("data-item-name");

        // モーダル内の input に値をセット
        document.getElementById("edit-item-id").value = itemId;
        document.getElementById("edit-item-name").value = itemName;
    });
});