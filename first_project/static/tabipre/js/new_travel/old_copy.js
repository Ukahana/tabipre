document.addEventListener("change", function (e) {
    if (!e.target.matches(".form-check-input")) return;

    // チェックされた項目のカテゴリ UL を取得
    const li = e.target.closest("li");
    const ul = li.closest("ul");

    // カテゴリ内の全チェックボックス
    const checkboxes = ul.querySelectorAll(".form-check-input");

    // チェック済み数を数える
    let checkedCount = 0;
    checkboxes.forEach(cb => {
        if (cb.checked) checkedCount++;
    });

    // バッジを書き換える
    const header = ul.previousElementSibling; // card-header
    const badge = header.querySelector(".badge");

    const totalCount = checkboxes.length;
    badge.textContent = `${checkedCount} / ${totalCount}`;
});