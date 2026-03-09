// ================================
// モーダルを開く処理（POST してから開く）
// ================================
document.addEventListener("DOMContentLoaded", function() {
    const openBtn = document.getElementById("open-modal-btn");
    const modal = document.getElementById("copyModal");

    // -------------------------------
    // 「前回テンプレートをコピー」ボタン → POST してモーダルを開く準備
    // -------------------------------
    if (openBtn) {
        openBtn.addEventListener("click", function() {
            const form = document.querySelector(".travel_step2_form");
            if (!form) return;

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

    if (flag === "true" && modal) {
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }

    // ================================
    // 「その他」チェック時のフォーム表示（HTML構造に完全対応）
    // ================================

    // 「その他」の label
    const otherLabel = document.querySelector(".transport-other");

    // その直前の <span class="form-check"> の中に input がある
    const otherCheckbox = otherLabel?.previousElementSibling?.querySelector("input[type='checkbox']");

    // 入力欄
    const otherBox = document.querySelector(".transport-other-box");

    if (otherCheckbox && otherBox) {

        // チェックしたら表示/非表示
        otherCheckbox.addEventListener("change", function () {
            otherBox.style.display = this.checked ? "inline" : "none";
        });

        // 初期状態でチェックされていたら表示
        if (otherCheckbox.checked) {
            otherBox.style.display = "inline";
        }
    }
});