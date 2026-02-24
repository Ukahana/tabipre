document.addEventListener("DOMContentLoaded", () => {

    //  星アイコン（お気に入り）
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

    //  continueModal が存在するなら自動で開く
    const modalEl = document.getElementById("continueModal");
    if (modalEl && modalEl.dataset.auto === "true") {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }

    //  カラーパレット
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

    // ★★★ 項目追加モーダルに category_id をセット ★★★
    const addItemButtons = document.querySelectorAll(".add-item-btn");
    const categoryInput = document.getElementById("modalCategoryId");

    if (categoryInput && addItemButtons.length > 0) {
        addItemButtons.forEach(btn => {
            btn.addEventListener("click", () => {
                categoryInput.value = btn.dataset.categoryId;
            });
        });
    }

    // ★★★ エラーがある場合は addItemModal を自動で開く ★★★
    setTimeout(() => {
        const hasError = document.querySelector(".errorlist");
        const addItemModal = document.getElementById("addItemModal");

        if (hasError && addItemModal) {
            const modal = new bootstrap.Modal(addItemModal);
            modal.show();
        }
    }, 50);

});