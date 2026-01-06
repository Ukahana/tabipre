document.addEventListener("DOMContentLoaded", () => {

    // すべてのチェックボックスにイベントを付与
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        checkbox.addEventListener("change", () => {
            const li = checkbox.closest("li");
            const ul = li.parentElement;

            // ① チェック状態で並び替え
            if (checkbox.checked) {
                ul.appendChild(li);  // 下へ移動
            } else {
                ul.insertBefore(li, ul.firstChild);  // 上へ戻す
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