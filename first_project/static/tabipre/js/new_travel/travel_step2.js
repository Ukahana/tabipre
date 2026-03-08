// ================================
// モーダルを開く処理
// ================================
document.addEventListener("DOMContentLoaded", function() {
    const openBtn = document.getElementById("open-modal-btn");
    const modal = document.getElementById("copyModal"); 

    if (openBtn && modal) {
        openBtn.addEventListener("click", function() {
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
        });
    }
});