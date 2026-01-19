// ⭐ お気に入り「決定」ボタン
document.getElementById("favoriteSelectBtn").addEventListener("click", function () {
    const selected = document.querySelector(".favorite-radio:checked");

    if (selected) {
        document.getElementById("itemNameInput").value = selected.value;

        // ⭐ モーダルを閉じる処理（Bootstrap 5）
        const modalEl = document.getElementById("favoriteModal");
        const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
        modal.hide();
    }
});


// ⭐ 星アイコン切り替え
const star = document.getElementById("favoriteStar");
const favValue = document.getElementById("favoriteValue");

if (star) {
    star.addEventListener("click", function () {
        const isOn = favValue.value === "1";
        star.src = isOn ? star.dataset.off : star.dataset.on;
        favValue.value = isOn ? "0" : "1";
    });
}

// ⭐ カラーパレット（色選択）
const colorOptions = document.querySelectorAll(".color-option");
const selectedColorInput = document.getElementById("selectedColor");

colorOptions.forEach(option => {
    option.addEventListener("click", function () {

        // 全ての選択状態を解除
        colorOptions.forEach(o => o.classList.remove("selected"));

        // クリックした色を選択状態に
        this.classList.add("selected");

        // hidden に値をセット
        selectedColorInput.value = this.dataset.value;
    });
});