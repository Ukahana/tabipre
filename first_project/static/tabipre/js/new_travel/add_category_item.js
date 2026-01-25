document.addEventListener("DOMContentLoaded", () => {

    // ⭐ 星アイコン（お気に入り）
    const star = document.getElementById("favoriteStar");
    const favValue = document.getElementById("favoriteValue");

    if (star && favValue) {
        star.src = star.dataset.off;
        favValue.value = "0";

        star.addEventListener("click", () => {
            const isOn = favValue.value === "1";
            star.src = isOn ? star.dataset.off : star.dataset.on;
            favValue.value = isOn ? "0" : "1";
        });
    }

    // ⭐ continueModal が存在するなら自動で開く
    const modalEl = document.getElementById("continueModal");
    if (modalEl) {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }

    // ⭐ カラーパレットの選択処理
    const colorOptions = document.querySelectorAll(".color-option");
    const selectedColor = document.getElementById("selectedColor");

    if (selectedColor && colorOptions.length > 0) {
        colorOptions.forEach(option => {
            option.addEventListener("click", () => {

                // 値をセット
                selectedColor.value = option.dataset.value;

                // 見た目の選択状態を更新
                colorOptions.forEach(o => o.classList.remove("selected"));
                option.classList.add("selected");
            });
        });
    }
});