document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("editItemModal");
    if (!modal) return;

    modal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;

        const itemId = button.getAttribute("data-item-id");
        const itemName = button.getAttribute("data-item-name");

        const form = modal.querySelector("form");
        form.action = `/item/edit/${itemId}/`;

        const input = modal.querySelector("input[name='item_name']");
        input.value = itemName;
    });

    // ⭐ モーダルが完全に表示された後にカーソル移動
    modal.addEventListener("shown.bs.modal", function () {
        const input = modal.querySelector("input[name='item_name']");
        const len = input.value.length;

        input.focus();
        input.setSelectionRange(len, len);  // ← これが確実
    });
});