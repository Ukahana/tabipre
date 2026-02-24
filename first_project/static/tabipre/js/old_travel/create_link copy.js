document.addEventListener("DOMContentLoaded", function () {

    /* ============================
       Flatpickr 初期化（衝突防止版）
    ============================ */
    const dateInput = document.getElementById("id_expiration_date");

    let fp = null;

    if (dateInput) {
        if (dateInput._flatpickr) {
            fp = dateInput._flatpickr;
        } else {
            fp = flatpickr(dateInput, {
                dateFormat: "Y-m-d",
                altInput: true,
                altFormat: "Y/m/d",
                altInputClass: "flatpickr-alt-input",
                allowInput: true,
                locale: "ja",

                parseDate: (value, format) => {
                    if (!value) return null;

                    const nums = value.replace(/[^\d]/g, "");
                    const currentYear = new Date().getFullYear();

                    if (nums.length === 2) {
                        return new Date(currentYear, nums[0] - 1, nums[1]);
                    }

                    if (nums.length === 4) {
                        return new Date(currentYear, nums.slice(0, 2) - 1, nums.slice(2, 4));
                    }

                    return flatpickr.parseDate(value, format);
                },

                clickOpens: false,
            });
        }
    }

    /* ============================
       モーダル処理（コピー機能）
    ============================ */
    if (window.SHOW_MODAL === true) {

        const modalEl = document.getElementById("linkModal");  // ← HTML と一致

        if (modalEl) {
            const modal = new bootstrap.Modal(modalEl);

            modalEl.addEventListener("shown.bs.modal", () => {

                const copyBtn = document.getElementById("copy_btn");   // ← HTML と一致
                const shareInput = document.getElementById("share_url"); // ← HTML と一致

                if (!copyBtn || !shareInput) return;

                copyBtn.addEventListener("click", () => {
                    navigator.clipboard.writeText(shareInput.value)
                        .then(() => {
                            const toastEl = document.getElementById("copyToast");
                            if (toastEl) new bootstrap.Toast(toastEl).show();
                        })
                        .catch(() => {
                            const toastEl = document.getElementById("copyToastError");
                            if (toastEl) new bootstrap.Toast(toastEl).show();
                        });
                });
            });

            modal.show();
        }
    }
});