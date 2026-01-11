// 項目追加
document.getElementById("add-item").addEventListener("click", function() {
    const container = document.getElementById("items-container");
    const div = document.createElement("div");
    div.classList.add("input-group", "mb-2", "item-row");

    div.innerHTML = `
        <input type="text" name="items" class="form-control" placeholder="新しい項目">
        <button type="button" class="btn btn-outline-danger remove-item">×</button>
    `;

    container.appendChild(div);
});

// 削除ボタン
document.addEventListener("click", function(e) {
    if (e.target.classList.contains("remove-item")) {
        e.target.closest(".item-row").remove();
    }
});