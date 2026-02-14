document.addEventListener("DOMContentLoaded", () => {

    // ============================
    // ★ カラー選択（修正版）
    // ============================
    const colorOptions = document.querySelectorAll(".color-option");
    const colorInput = document.getElementById("id_category_color");

    if (colorInput && colorOptions.length > 0) {
        colorOptions.forEach(option => {
            option.addEventListener("click", () => {
                colorInput.value = option.dataset.value;
                colorOptions.forEach(o => o.classList.remove("selected"));
                option.classList.add("selected");
            });
        });
    }

    // ============================
    // ★ 登録ボタン → continue=0 で送信
    // ============================
    const submitBtn = document.getElementById("validateBeforeModal");
    const form = document.getElementById("categoryItemForm");
    const continueFlag = document.getElementById("continueFlag");

    if (submitBtn && form && continueFlag) {
        submitBtn.addEventListener("click", () => {
            continueFlag.value = "0";
            form.submit();   
        });
    }

});