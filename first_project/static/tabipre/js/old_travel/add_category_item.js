document.addEventListener("DOMContentLoaded", () => {

    // ⭐ お気に入りスターの ON/OFF
    const star = document.getElementById("favoriteStar");
    const favValue = document.getElementById("favoriteValue");

    if (star && favValue) {
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

    // ⭐ 登録ボタン → 最小限のバリデーション（分類名だけチェック）
    const openModalButton = document.getElementById("openModalButton");

    if (openModalButton) {
        openModalButton.addEventListener("click", () => {

            const categoryNameInput = document.querySelector("input[name='category_name']");
            const categoryName = categoryNameInput.value.trim();

            // 赤枠リセット
            categoryNameInput.classList.remove("is-invalid");

            // ⭐ 分類名チェック（空なら submit しない）
            if (!categoryName) {
                categoryNameInput.classList.add("is-invalid");
                return;
            }

            // OKならフォーム送信（Django が残りをチェック）
            document.getElementById("categoryItemForm").submit();
        });
    }

    // ⭐ Django success=1 のときだけモーダルを開く
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get("success") === "1") {
        const modal = new bootstrap.Modal(document.getElementById("continueModal"));
        modal.show();
    }

});