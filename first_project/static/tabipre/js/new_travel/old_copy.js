document.addEventListener("change", function (e) {
    if (!e.target.classList.contains("form-check-input")) return;

    // チェックされた項目の <li>
    const li = e.target.closest("li");
    if (!li) return;

    // 親の <ul>（カテゴリの項目リスト）
    const ul = li.closest("ul");
    if (!ul) return;

    // カテゴリ内の全チェックボックス
    const checkboxes = ul.querySelectorAll(".form-check-input");

    // チェック済み数
    const checkedCount = [...checkboxes].filter(cb => cb.checked).length;
    const totalCount = checkboxes.length;

    // カテゴリのヘッダー（card-header）
    const header = ul.closest(".card").querySelector(".card-header");
    if (!header) return;

    // バッジ（checked / total）
    const badge = header.querySelector(".badge");
    if (!badge) return;

    badge.textContent = `${checkedCount} / ${totalCount}`;
});
document.addEventListener("DOMContentLoaded", function() {
    const memo = document.querySelector("textarea[name='memo']");
    if (memo) {
        setTimeout(() => {
            memo.focus();  // フォーカス
            memo.selectionStart = memo.value.length; // 文末へ
            memo.selectionEnd = memo.value.length;
        }, 150); // collapse のアニメーション対策
    }
});