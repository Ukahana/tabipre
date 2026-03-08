// ================================
// モーダルを開く処理（POST してから開く）
// ================================
document.addEventListener("DOMContentLoaded", function() {
    const openBtn = document.getElementById("open-modal-btn");
    const modal = document.getElementById("copyModal");

    if (openBtn && modal) {
        openBtn.addEventListener("click", function() {
            const form = document.querySelector(".travel_step2_form");

            // hidden input を追加して action=open_modal を送る
            const input = document.createElement("input");
            input.type = "hidden";
            input.name = "action";
            input.value = "open_modal";
            form.appendChild(input);

            form.submit();
        });
    }

    // -------------------------------
    // Django が open_modal=True を返したときにモーダルを開く
    // -------------------------------
    const flag = document.getElementById("modal-flag")?.dataset.openModal;
    if (flag === "true") {
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }
});