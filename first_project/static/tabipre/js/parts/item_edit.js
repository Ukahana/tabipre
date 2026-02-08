document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("editItemModal");
    if (!modal) return;

    modal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;

        // HTML の data 属性に合わせる
        const itemId = button.dataset.itemId;
        const itemName = button.dataset.itemName;

        // hidden にセット
        document.getElementById("editItemId").value = itemId;
        document.getElementById("editItemInput").value = itemName;

        // ★★★ ここが最重要 ★★★
        // edit_item の URL を動的にセット
        const form = document.getElementById("editItemForm");
        form.action = `/item/edit/${itemId}/`;
    });

    modal.addEventListener("shown.bs.modal", function () {
        const input = document.getElementById("editItemInput");
        const len = input.value.length;

        input.focus();
        input.setSelectionRange(len, len);
    });
});