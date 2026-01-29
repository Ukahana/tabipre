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

    // ⭐ continueModal が存在するなら自動で開く（saved=1 用）
    const modalEl = document.getElementById("continueModal");
    if (modalEl && modalEl.dataset.auto === "true") {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }

    // ⭐ カラーパレットの選択処理
    const colorOptions = document.querySelectorAll(".color-option");
    const selectedColor = document.getElementById("selectedColor");

    if (selectedColor && colorOptions.length > 0) {
        colorOptions.forEach(option => {
            option.addEventListener("click", () => {
                selectedColor.value = option.dataset.value;
                colorOptions.forEach(o => o.classList.remove("selected"));
                option.classList.add("selected");
            });
        });
    }

    // ⭐ 登録ボタン → continueModal を開く（今回必要な処理）
    const openBtn = document.getElementById("openContinueModal");
    if (openBtn) {
        openBtn.addEventListener("click", () => {
            const modalEl = document.getElementById("continueModal");
            if (modalEl) {
                const modal = new bootstrap.Modal(modalEl);
                modal.show();
            }
        });
    }

});