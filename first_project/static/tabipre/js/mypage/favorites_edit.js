// 項目追加
document.getElementById("add-item").addEventListener("click", function () {
    const container = document.querySelector(".edit-list");

    // ★ すべての input をチェックして、空欄が1つでもあれば追加しない
    const inputs = container.querySelectorAll("input[name='items']");
    for (const input of inputs) {
        if (input.value.trim() === "") {
            input.focus();
            return;
        }
    }

    // 新しい項目を追加
    const li = document.createElement("li");
    li.classList.add("item-row");

    li.innerHTML = `
        <span class="dot">・</span>
        <input type="text" name="items" class="form-control item-input" placeholder="項目を入力">
        <button type="button" class="remove-item">×</button>
    `;

    container.appendChild(li);

    // 一番下までスクロール
    container.scrollTop = container.scrollHeight;
});

// 削除ボタン（動的追加にも対応）
document.addEventListener("click", function (e) {
    if (e.target.classList.contains("remove-item")) {
        e.target.closest(".item-row").remove();
    }
});