// ⭐ お気に入りトグル（画像版）
// ===============================
let starImg;
let favoriteFlag;

document.addEventListener("DOMContentLoaded", () => {
    const star = document.getElementById("favorite_star");
    starImg = document.getElementById("favorite_star_img");
    favoriteFlag = document.getElementById("favorite_flag");

    star.addEventListener("click", () => {
        if (favoriteFlag.value === "0") {
            favoriteFlag.value = "1";
            starImg.src = "/static/tabipre/icons/star_on.png";
        } else {
            favoriteFlag.value = "0";
            starImg.src = "/static/tabipre/icons/star_off.png";
        }
    });
});


// ===============================
// お気に入りモーダル → 項目名に反映
// ===============================
document.querySelectorAll(".favorite-item").forEach(btn => {
    btn.addEventListener("click", () => {
        document.getElementById("item_name").value = btn.dataset.name;
        const modal = bootstrap.Modal.getInstance(document.getElementById("favoriteModal"));
        modal.hide();
    });
});


// ===============================
// 分類名オートコンプリート
// ===============================
const categoryInput = document.getElementById("category_name");
const categoryBox = document.getElementById("category_suggestions");

categoryInput.addEventListener("input", () => {
    const q = categoryInput.value.trim();
    if (!q) {
        categoryBox.innerHTML = "";
        return;
    }

    fetch(`/autocomplete/category/?q=${encodeURIComponent(q)}`)
        .then(res => res.json())
        .then(data => {
            categoryBox.innerHTML = "";
            data.forEach(name => {
                const item = document.createElement("button");
                item.className = "list-group-item list-group-item-action";
                item.textContent = name;
                item.onclick = () => {
                    categoryInput.value = name;
                    categoryBox.innerHTML = "";
                };
                categoryBox.appendChild(item);
            });
        });
});


// ===============================
// 項目名オートコンプリート
// ===============================
const itemInput = document.getElementById("item_name");
const itemBox = document.getElementById("item_suggestions");

itemInput.addEventListener("input", () => {
    const q = itemInput.value.trim();
    if (!q) {
        itemBox.innerHTML = "";
        return;
    }

    fetch(`/autocomplete/item/?q=${encodeURIComponent(q)}`)
        .then(res => res.json())
        .then(data => {
            itemBox.innerHTML = "";
            data.forEach(name => {
                const item = document.createElement("button");
                item.className = "list-group-item list-group-item-action";
                item.textContent = name;
                item.onclick = () => {
                    itemInput.value = name;
                    itemBox.innerHTML = "";
                };
                itemBox.appendChild(item);
            });
        });
});


// ===============================
// フォーカス外れたら候補を消す
// ===============================
document.addEventListener("click", (e) => {
    if (!categoryInput.contains(e.target)) {
        categoryBox.innerHTML = "";
    }
    if (!itemInput.contains(e.target)) {
        itemBox.innerHTML = "";
    }
});


// ===============================
// ② カラーパレット（丸い色選択）
// ===============================
document.querySelectorAll(".color-option").forEach(option => {
    option.addEventListener("click", () => {
        document.querySelectorAll(".color-circle").forEach(c => {
            c.classList.remove("selected");
        });
        option.querySelector(".color-circle").classList.add("selected");
    });
});


// ===============================
// ① 保存後の「追加を続けますか？」モーダル表示
// ===============================
document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    if (params.get("saved") === "1") {
        const modal = new bootstrap.Modal(document.getElementById("continueModal"));
        modal.show();
    }});

// ===============================
// ③ 「はい（続けて追加）」 → フォームをクリア
// ===============================
const continueBtn = document.getElementById("continueBtn");

if (continueBtn) {
    continueBtn.addEventListener("click", () => {
        // フォームをクリア
        document.getElementById("category_name").value = "";
        document.getElementById("item_name").value = "";
        favoriteFlag.value = "0";
        starImg.src = "/static/tabipre/icons/star_off.png";

        // カラーパレットもリセット
        document.querySelectorAll(".color-radio").forEach(r => r.checked = false);
        document.querySelectorAll(".color-circle").forEach(c => c.classList.remove("selected"));

        // モーダルを閉じる
        const modal = bootstrap.Modal.getInstance(document.getElementById("continueModal"));
        modal.hide();

        // URL の ?saved=1 を削除
        history.replaceState(null, "", window.location.pathname);
    });
}