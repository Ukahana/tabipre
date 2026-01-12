console.log("add_item.js 読み込まれた！");
document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("addItemModal");

    modal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        const categoryId = button.getAttribute("data-category-id");

        // hidden input にセット
        document.getElementById("modalCategoryId").value = categoryId;

        // ⭐ 星の初期化とイベント付け直し
        const star = document.getElementById("favoriteStar");
        const favValue = document.getElementById("favoriteValue");

        star.src = star.dataset.off;
        favValue.value = "0";

        star.onclick = function () {
            const isOn = favValue.value === "1";
            star.src = isOn ? star.dataset.off : star.dataset.on;
            favValue.value = isOn ? "0" : "1";
        };
    });
});