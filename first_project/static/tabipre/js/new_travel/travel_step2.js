document.addEventListener("DOMContentLoaded", () => {

    // -----------------------------
    // その他の表示切替
    // -----------------------------
    const otherCheckbox = document.querySelector('.transport-other input[type="checkbox"]');
    const otherBox = document.querySelector('.transport-other-box');

    if (otherCheckbox && otherBox) {
        const toggleOtherBox = () => {
            otherBox.style.display = otherCheckbox.checked ? "inline-block" : "none";
        };

        otherCheckbox.addEventListener("change", toggleOtherBox);
        toggleOtherBox(); // 初期表示
    }

    // -----------------------------
    // モーダル自動オープン
    // -----------------------------
    const flagElement = document.getElementById("modal-flag");
    const modalFlag = flagElement?.dataset.openModal;

    if (modalFlag === "true") {
        const modal = new bootstrap.Modal(document.getElementById("copyModal"));
        modal.show();
    }
});