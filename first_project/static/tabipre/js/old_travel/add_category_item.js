document.addEventListener("DOMContentLoaded", () => {

    // ⭐ お気に入りスターの ON/OFF
    const star = document.getElementById("favoriteStar");
    const favValue = document.getElementById("favoriteValue");

    if (star && favValue) {
        // 初期状態を hidden の値から反映
        const isOn = favValue.value === "1";
        star.src = isOn ? star.dataset.on : star.dataset.off;

        star.addEventListener("click", () => {
            const nowOn = favValue.value === "1";
            favValue.value = nowOn ? "0" : "1";
            star.src = nowOn ? star.dataset.off : star.dataset.on;
        });
    }

    // ⭐ お気に入りモーダルの「登録」ボタン
    document.addEventListener("click", (e) => {
        if (e.target.id === "favoriteSelectBtn") {

            const selected = document.querySelector(".favorite-radio:checked");
            if (!selected) return;

            const itemInput = document.getElementById("itemNameInput");
            if (itemInput) {
                itemInput.value = selected.value;
            }

            const modalEl = document.getElementById("favoriteModal");
            const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            modal.hide();
        }
    });

    // ⭐ カラーパレットの選択
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

    // ⭐ continueModal の自動オープン（必要な場合のみ）
    const modalEl = document.getElementById("continueModal");
    if (modalEl && modalEl.dataset.auto === "true") {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }

});