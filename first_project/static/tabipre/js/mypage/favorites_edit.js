// ------------------------------
// 項目追加ボタン
// ------------------------------
document.getElementById("add-item").addEventListener("click", function () {
    const container = document.querySelector(".edit-list");
    const errorList = document.getElementById("errorlist");

    // エラーリセット
    errorList.style.display = "none";
    errorList.innerHTML = "";

    const inputs = container.querySelectorAll(".item-input");
    let hasError = false;

    // 空欄チェック
    inputs.forEach(input => {
        input.classList.remove("is-invalid");

        if (input.value.trim() === "") {
            input.classList.add("is-invalid");
            hasError = true;
        }
    });

    if (hasError) {
        errorList.innerHTML = "<li>空欄の項目があります。</li><li>入力してから追加してください。</li>";
        errorList.style.display = "block";
        return;
    }

    // 新しい項目を追加
    const li = document.createElement("li");
    li.classList.add("item-row");

    li.innerHTML = `
        <span class="dot">・</span>
        <input type="text" class="form-control item-input" placeholder="項目を入力">
        <button type="button" class="remove-item">×</button>
    `;

    container.appendChild(li);
    container.scrollTop = container.scrollHeight;
});


// ------------------------------
// 削除ボタン（×）
// ------------------------------
document.addEventListener("click", function (e) {
    if (e.target.classList.contains("remove-item")) {
        e.target.closest(".item-row").remove();
    }
});


// ------------------------------
// 保存前に hidden にまとめる
// ------------------------------
document.querySelector("form").addEventListener("submit", function () {
    const inputs = document.querySelectorAll(".item-input");
    const hidden = document.getElementById("items-hidden");
    const values = [];

    inputs.forEach(input => {
        const v = input.value.trim();
        if (v !== "") {
            values.push(v);
        }
    });

    hidden.value = values.join("||");
});