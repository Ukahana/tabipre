document.addEventListener("DOMContentLoaded", () => {

    // すべてのカードを処理
    document.querySelectorAll(".card").forEach(card => {

        const checkboxes = card.querySelectorAll("input[type='checkbox'][name^='item_checked_']");
        const badge = card.querySelector(".badge");

        // badge が無い or チェックボックスが無いカードはスキップ
        if (!badge || checkboxes.length === 0) return;

        // 初期表示
        updateCount();

        // チェック変更時に更新
        checkboxes.forEach(cb => {
            cb.addEventListener("change", updateCount);
        });

        // カウント更新関数
        function updateCount() {
            const total = checkboxes.length;
            const checked = [...checkboxes].filter(cb => cb.checked).length;
            badge.textContent = `${checked} / ${total}`;
        }
    });

});