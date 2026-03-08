document.addEventListener("DOMContentLoaded", () => {

    //  お気に入りスターの ON/OFF 
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

    //  項目追加モーダルに category_id をセット 
    const addItemButtons = document.querySelectorAll(".add-item-btn");
    const categoryInput = document.getElementById("modalCategoryId");

    if (categoryInput && addItemButtons.length > 0) {
        addItemButtons.forEach(btn => {
            btn.addEventListener("click", () => {
                categoryInput.value = btn.dataset.categoryId;
            });
        });
    }

    //  エラーがある場合は addItemModal を自動で開く 
    setTimeout(() => {
        const hasError = document.querySelector(".errorlist");
        const addItemModal = document.getElementById("addItemModal");

        if (hasError && addItemModal) {
            const modal = new bootstrap.Modal(addItemModal);
            modal.show();
        }
    }, 50);

});