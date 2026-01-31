// ===============================
// ダブルタップ防止（collapse のみ）
// ===============================
document.addEventListener('dblclick', function(e) {
    // collapse トリガーだけ防止
    if (e.target.closest('[data-bs-toggle="collapse"]')) {
        e.stopPropagation();
        e.preventDefault();
    }
}, true);


// ===============================
// collapse 暴発防止
// ===============================
document.addEventListener('click', function(e) {
    const trigger = e.target.closest('[data-bs-toggle="collapse"]');
    if (trigger) {
        if (!e.target.matches('[data-bs-toggle="collapse"]')) {
            e.stopPropagation();
        }
    }
}, true);


// ===============================
// Enter キー送信防止（input[type=text] のみ）
// ===============================
document.addEventListener('keydown', function(e) {
    const tag = e.target.tagName.toLowerCase();

    // ⭐ テキスト入力欄だけ Enter を無効化
    if (e.key === 'Enter' && tag === 'input' && e.target.type === 'text') {
        e.preventDefault();
    }
}, true);