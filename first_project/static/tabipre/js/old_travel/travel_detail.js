// CSRFトークン取得
function getCookie(name) {
    for (const cookie of document.cookie.split(";")) {
        const c = cookie.trim();
        if (c.startsWith(name + "=")) {
            return decodeURIComponent(c.substring(name.length + 1));
        }
    }
    return null;
}

// チェック処理
function toggleItem(checkbox, itemId) {
    const pos = window.scrollY;

    fetch(`/tabipre/toggle_item/${itemId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ checked: checkbox.checked })
    }).then(() => {
        window.scrollTo(0, pos);
        updateCategoryCount(checkbox);
        updateTotalCount();
        updateStatus();   // ← travelStatus を更新
    });
}

// カテゴリ内の分数更新
function updateCategoryCount(checkbox) {
    const ul = checkbox.closest("ul");
    if (!ul) return;

    const all = ul.querySelectorAll('.form-check-input');
    const checked = ul.querySelectorAll('.form-check-input:checked');

    const badge = ul.closest('.card').querySelector('.category-badge');
    if (badge) badge.textContent = `${checked.length} / ${all.length}`;
}

// 全体の分数更新
function updateTotalCount() {
    const all = document.querySelectorAll('.form-check-input');
    const checked = document.querySelectorAll('.form-check-input:checked');

    const total = document.getElementById('totalCheckCount');
    if (total) total.textContent = `${checked.length} / ${all.length}`;
}

// ステータス更新（未 / 完 / 済）
function updateStatus() {
    console.log("updateStatus called");

    // ← travelStatus-◯◯ を参照
    const statusEl = document.getElementById(`travelStatus-${travelId}`);
    if (!statusEl) {
        console.log("statusEl not found");
        return;
    }

    const endDate = new Date(statusEl.dataset.endDate);
    const today = new Date();

    const all = document.querySelectorAll('.form-check-input');
    const checked = document.querySelectorAll('.form-check-input:checked');

    console.log("all:", all.length, "checked:", checked.length);

    // 旅行終了日が過ぎていたら常に「済」
    if (today > endDate) {
        setStatus(statusEl, "済");
        return;
    }

    // 終了日前 → 未 or 完
    const isAllChecked = (checked.length === all.length && all.length > 0);
    setStatus(statusEl, isAllChecked ? "完" : "未");
}

// ステータス表示の共通処理
function setStatus(el, status) {
    console.log("setStatus:", status);

    el.textContent = status;
    el.classList.remove("status-mi", "status-kan", "status-zumi");

    if (status === "未") el.classList.add("status-mi");
    if (status === "完") el.classList.add("status-kan");
    if (status === "済") el.classList.add("status-zumi");
}

// ページ読み込み時にも実行
document.addEventListener("DOMContentLoaded", () => {
    updateTotalCount();
    updateStatus();
});