document.addEventListener("DOMContentLoaded", () => {

    // 並び替え関数（未チェック → チェック済み）
    function reorderItems(ul) {
        const allItems = Array.from(ul.querySelectorAll("li"));
        const checkedItems = allItems.filter(li => li.querySelector('input[type="checkbox"]').checked);
        const uncheckedItems = allItems.filter(li => !li.querySelector('input[type="checkbox"]').checked);

        ul.innerHTML = "";
        uncheckedItems.forEach(li => ul.appendChild(li));
        checkedItems.forEach(li => ul.appendChild(li));
    }

    // チェックボックス処理
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {

        const itemId = checkbox.name.replace("item_checked_", "");

        // 保存された状態を復元
        const saved = localStorage.getItem("checked_" + itemId);
        if (saved !== null) {
            checkbox.checked = saved === "1";
        }

        // 変更時に保存＋並び替え
        checkbox.addEventListener("change", () => {
            localStorage.setItem("checked_" + itemId, checkbox.checked ? "1" : "0");

            const ul = checkbox.closest("ul");
            reorderItems(ul);
        });
    });

    // 名前編集の保存・復元
    document.querySelectorAll('input[type="text"][name^="rename_"]').forEach(input => {

        const itemId = input.name.replace("rename_", "");

        // 復元
        const saved = localStorage.getItem("name_" + itemId);
        if (saved !== null) {
            input.value = saved;
        }

        // 入力時に保存
        input.addEventListener("input", () => {
            localStorage.setItem("name_" + itemId, input.value);
        });
    });

    // ページ読み込み時に全カテゴリを並び替え
    document.querySelectorAll("ul.list-group").forEach(ul => reorderItems(ul));

});