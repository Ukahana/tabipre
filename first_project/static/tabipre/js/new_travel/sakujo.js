document.addEventListener("DOMContentLoaded", function () {

    // ⭐ show_continue_modal が True のときモーダルを表示
    const continueModal = document.getElementById("continueModal");
    if (continueModal) {
        const modal = new bootstrap.Modal(continueModal);
        modal.show();
    }
});