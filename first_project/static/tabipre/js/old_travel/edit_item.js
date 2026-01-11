document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("editItemModal");
    if (!modal) return;

    modal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;

        const itemId = button.getAttribute("data-item-id");
        const itemName = button.getAttribute("data-item-name");

        const form = modal.querySelector("form");

        // URL を直接セット
        form.action = `/item/edit/${itemId}/`;

        // 入力欄に値をセット
        modal.querySelector("input[name='item_name']").value = itemName;
    });
});