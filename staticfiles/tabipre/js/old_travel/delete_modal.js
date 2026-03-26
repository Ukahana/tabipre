document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll(
          ".delete-category-btn, .delete-template-btn"
    );

    const inputCategory = document.getElementById("deleteCategoryInput");
    const inputItem = document.getElementById("deleteItemInput");
    const inputTemplate = document.getElementById("deleteTemplateInput");

    const deleteMessage = document.getElementById("deleteMessage");

    deleteButtons.forEach(btn => {
        btn.addEventListener("click", function () {

            // hidden input をクリア
            inputCategory.value = "";
            inputItem.value = "";
            inputTemplate.value = "";

            const type = this.dataset.type;
            const id = this.dataset.id;
            const name = this.dataset.name;

            // 文言切り替え
            if (type === "category") {
                deleteMessage.textContent = `分類「${name}」を削除しますか？`;
                inputCategory.value = id;
            }

            if (type === "template") {
                deleteMessage.textContent = `テンプレートを削除しますか？`;
                inputTemplate.value = id;
            }
        });
    });

});