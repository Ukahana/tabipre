document.addEventListener("DOMContentLoaded", () => {

    const colorOptions = document.querySelectorAll(".color-option");
    const selectedColor = document.getElementById("selectedColor");

    if (!selectedColor || colorOptions.length === 0) return;

    colorOptions.forEach(option => {
        option.addEventListener("click", () => {

            // hidden に値をセット
            selectedColor.value = option.dataset.value;

            // 選択状態の見た目を更新
            colorOptions.forEach(o => o.classList.remove("selected"));
            option.classList.add("selected");
        });
    });

});