document.addEventListener("DOMContentLoaded", () => {

    // ============================
    // ★ カラー選択
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
    // ★ 登録ボタン → まずバリデーション送信
    // ============================
    const submitBtn = document.getElementById("validateBeforeModal");
    const form = document.getElementById("categoryItemForm");
    const continueFlag = document.getElementById("continueFlag");

    if (submitBtn && form && continueFlag) {
        submitBtn.addEventListener("click", () => {

            // 「はい」前提で送信
            continueFlag.value = "1";

            // Django に POST → バリデーション実行
            form.submit();
        });
    }
});