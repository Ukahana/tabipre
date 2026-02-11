window.submitCategoryForm = function(action) {

    const form = document.getElementById("categoryItemForm");
    const flag = document.getElementById("continueFlag");

    if (action === "first") {
        flag.value = "0";   // バリデーション
    } else if (action === "continue") {
        flag.value = "1";   // はい（保存）
    } else if (action === "cancel") {
        flag.value = "2";   // いいえ（戻る）
    }

    form.submit();
};