/* ================================
   チェック更新 → バッジの数字更新
================================ */
document.addEventListener("change", function (e) {
    if (!e.target.classList.contains("form-check-input")) return;

    const li = e.target.closest("li");
    if (!li) return;

    const ul = li.closest("ul");
    if (!ul) return;

    const checkboxes = ul.querySelectorAll(".form-check-input");
    const checkedCount = [...checkboxes].filter(cb => cb.checked).length;
    const totalCount = checkboxes.length;

    const header = ul.closest(".card").querySelector(".card-header");
    if (!header) return;

    const badge = header.querySelector(".badge");
    if (!badge) return;

    badge.textContent = `${checkedCount} / ${totalCount}`;
});


/* ================================
   画面読み込み時 → メモにフォーカス & 文末へ
================================ */
document.addEventListener("DOMContentLoaded", function() {
    const memo = document.querySelector("textarea[name='memo']");
    if (memo) {
        setTimeout(() => {
            memo.focus();
            const len = memo.value.length;
            memo.selectionStart = len;
            memo.selectionEnd = len;
        }, 150); // collapse アニメ対策
    }
});