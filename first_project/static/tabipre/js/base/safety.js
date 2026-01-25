// ダブルタップ防止（スマホで collapse や submit が暴発するのを防ぐ）
document.addEventListener('dblclick', function(e) {
    e.stopPropagation();
    e.preventDefault();
}, true);

// collapse 暴発防止（入力欄や削除ボタンをタップしても collapse が閉じない）
document.addEventListener('click', function(e) {
    const trigger = e.target.closest('[data-bs-toggle="collapse"]');
    if (trigger) {
        // collapse トリガー以外の子要素のクリックは伝播させない
        if (!e.target.matches('[data-bs-toggle="collapse"]')) {
            e.stopPropagation();
        }
    }
}, true);

// Enter キー送信防止（スマホキーボードの Enter でフォーム送信されるのを防ぐ）
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
    }
}, true);