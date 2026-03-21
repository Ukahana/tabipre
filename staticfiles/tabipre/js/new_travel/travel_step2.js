document.addEventListener("DOMContentLoaded", function () {

    // ================================
    // ① 交通手段「その他」表示制御
    // ================================
    const otherLabel = document.querySelector(".transport-other");
    if (otherLabel) {
        const otherCheckbox = otherLabel.querySelector("input[type='checkbox']");
        const otherBox = otherLabel.querySelector(".transport-other-box");

        if (otherCheckbox && otherBox) {
            otherCheckbox.addEventListener("change", function () {
                otherBox.style.display = this.checked ? "inline" : "none";
            });

            if (otherCheckbox.checked) {
                otherBox.style.display = "inline";
            }
        }
    }

    // ================================
    // ② モーダルを開く処理（POST してから開く）
    // ================================
    const openBtn = document.getElementById("open-modal-btn");
    const modal = document.getElementById("copyModal");

    if (openBtn && modal) {
        openBtn.addEventListener("click", function () {
            const form = document.querySelector(".travel_step2_form");

            // hidden input を追加して action=open_modal を送る
            const input = document.createElement("input");
            input.type = "hidden";
            input.name = "action";
            input.value = "open_modal";
            form.appendChild(input);

            // ★ form.submit() は使わない（値が取りこぼされるため）
            // ★ 隠し submit ボタンを作ってクリックする
            const hiddenSubmit = document.createElement("button");
            hiddenSubmit.type = "submit";
            hiddenSubmit.style.display = "none";
            form.appendChild(hiddenSubmit);

            hiddenSubmit.click();
        });
    }

    // ================================
    // ③ Django が open_modal=True を返したときにモーダルを開く
    // ================================
    const flag = document.getElementById("modal-flag")?.dataset.openModal;
    if (flag === "true") {
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }
});