document.addEventListener("DOMContentLoaded", () => {

    // ============================
    // ⭐ 通常画面の星アイコン
    // ============================
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

    // ============================
    // ⭐ カラーパレット
    // ============================
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

    // ============================
    // ⭐ continueModal があれば自動表示
    // ============================
    const modalEl = document.getElementById("continueModal");
    if (modalEl) {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }

});
// ============================
// ⭐ モーダル内の星アイコン
// ============================
const addItemModal = document.getElementById("addItemModal");

if (addItemModal) {
    addItemModal.addEventListener("show.bs.modal", (event) => {

        const button = event.relatedTarget;
        const categoryId = button.getAttribute("data-category-id");

        document.getElementById("modalCategoryId").value = categoryId;

        const modalStar = document.getElementById("modalFavoriteStar");
        const modalFavValue = document.getElementById("modalFavoriteValue");

        modalStar.src = modalStar.dataset.off;
        modalFavValue.value = "0";

        modalStar.onclick = () => {
            const isOn = modalFavValue.value === "1";
            modalStar.src = isOn ? modalStar.dataset.off : modalStar.dataset.on;
            modalFavValue.value = isOn ? "0" : "1";
        };
    });
}