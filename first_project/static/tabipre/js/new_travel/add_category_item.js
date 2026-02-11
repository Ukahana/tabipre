document.addEventListener("DOMContentLoaded", () => {

    // ============================
    // ★ カラー選択（既存旅行と同じ動き）
    // ============================
    const colorOptions = document.querySelectorAll(".color-option");
    const selectedColor = document.getElementById("selectedColor");

    if (selectedColor && colorOptions.length > 0) {
        colorOptions.forEach(option => {
            option.addEventListener("click", () => {

                // hidden input に値をセット
                selectedColor.value = option.dataset.value;

                // 見た目の selected を更新
                colorOptions.forEach(o => o.classList.remove("selected"));
                option.classList.add("selected");
            });
        });
    }


    // ============================
    // ★ 星アイコン（既存旅行と同じ動き）
    // ============================
    const star = document.getElementById("favoriteStar");
    const favoriteFlag = document.getElementById("id_favorite_flag");

    if (star && favoriteFlag) {

        star.addEventListener("click", () => {

            const on = star.dataset.on;
            const off = star.dataset.off;

            // ON → OFF
            if (star.classList.contains("active")) {
                star.src = off;
                star.classList.remove("active");
                favoriteFlag.value = "0";

            // OFF → ON
            } else {
                star.src = on;
                star.classList.add("active");
                favoriteFlag.value = "1";
            }
        });
    }

});