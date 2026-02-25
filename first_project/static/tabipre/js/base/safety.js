document.addEventListener('click', function(e) {
    const trigger = e.target.closest('[data-bs-toggle="collapse"]');

    // collapse トリガー以外の部分をタップしたときに暴発しないようにする
    if (trigger && !e.target.matches('[data-bs-toggle="collapse"]')) {
        e.stopPropagation();
    }
}, true);