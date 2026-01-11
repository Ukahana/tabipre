document.addEventListener("DOMContentLoaded", function () {

    // ★ お気に入りスターの切り替え
    const star = document.getElementById("favoriteStar");
    const favValue = document.getElementById("favoriteValue");

    if (star) {
        star.addEventListener("click", function () {
            const isOn = favValue.value === "1";

            star.src = isOn ? star.dataset.off : star.dataset.on;
            favValue.value = isOn ? "0" : "1";
        });
    }

    // ★ 追加モーダルの categoryId セット
    const modal = document.getElementById("addItemModal");

    if (modal) {
        modal.addEventListener("show.bs.modal", function (event) {
            const button = event.relatedTarget;
            const categoryId = button.getAttribute("data-category-id");

            document.getElementById("modalCategoryId").value = categoryId;
        });
    }
});