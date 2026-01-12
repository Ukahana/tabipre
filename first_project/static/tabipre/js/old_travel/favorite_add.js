document.addEventListener("DOMContentLoaded", function () {

    // ⭐ お気に入り選択ボタン
    const favButtons = document.querySelectorAll(".favorite-select-btn");

    favButtons.forEach(btn => {
        btn.addEventListener("click", function () {
            const name = this.dataset.name;

            // 項目名に反映
            document.getElementById("itemNameInput").value = name;

            // モーダルを閉じる
            const modalEl = document.getElementById("favoriteModal");
            const modal = bootstrap.Modal.getInstance(modalEl);
            modal.hide();
        });
    });

    // ⭐ 星アイコン切り替え
    const star = document.getElementById("favoriteStar");
    const favValue = document.getElementById("favoriteValue");

    star.addEventListener("click", function () {
        const isOn = favValue.value === "1";
        star.src = isOn ? star.dataset.off : star.dataset.on;
        favValue.value = isOn ? "0" : "1";
    });
});