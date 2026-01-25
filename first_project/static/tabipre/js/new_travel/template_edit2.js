document.addEventListener("DOMContentLoaded", () => {

    // すべてのチェックボックスにイベントを付与
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener("change", () => {
            const li = checkbox.closest("li");
            const ul = li.parentElement;

            // ① チェック状態で並び替え
            if (checkbox.checked) {
                // チェック → 一番下へ
                ul.appendChild(li);
            } else {
                // 未チェック → 最初の「未チェック項目の直後」に戻す
                const firstChecked = ul.querySelector('input[type="checkbox"]:checked');
                if (firstChecked) {
                    ul.insertBefore(li, firstChecked.closest("li"));
                } else {
                    // 全部未チェックなら先頭へ
                    ul.insertBefore(li, ul.firstElementChild);
                }
            }

            // ② カテゴリのチェック数を更新
            updateCategoryCount(ul);
        });
    });

    // カテゴリのチェック数を更新する関数
    function updateCategoryCount(ul) {
        const items = ul.querySelectorAll("li");
        const checked = ul.querySelectorAll('input[type="checkbox"]:checked').length;

        const card = ul.closest(".card");
        const badge = card.querySelector(".badge");

        badge.textContent = `${checked} / ${items.length}`;
    }

});