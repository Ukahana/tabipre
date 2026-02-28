document.addEventListener("DOMContentLoaded", function () {

    // -----------------------------
    // 日付入力（flatpickr）
    // -----------------------------
    const dateInput = document.getElementById("id_expiration_date");

    let fp = null;
    let altInput = null;

    if (dateInput) {
        try {
            fp = flatpickr(dateInput, {
                dateFormat: "Y-m-d",
                altInput: true,
                altFormat: "Y/m/d",
                altInputClass: "flatpickr-alt-input",
                allowInput: true,
                locale: "ja",
                clickOpens: false,

                parseDate: (value, format) => {
                    if (!value) return null;

                    const nums = value.replace(/[^\d]/g, "");
                    const currentYear = new Date().getFullYear();

                    if (nums.length === 2) {
                        return new Date(currentYear, nums[0] - 1, nums[1]);
                    }
                    if (nums.length === 3) {
                        return new Date(currentYear, nums[0] - 1, nums.slice(1));
                    }
                    if (nums.length === 4) {
                        return new Date(currentYear, nums.slice(0, 2) - 1, nums.slice(2, 4));
                    }

                    return flatpickr.parseDate(value, format);
                }
            });

            altInput = fp.altInput;

            if (altInput) {
                altInput.addEventListener("blur", function () {
                    const raw = altInput.value.trim();

                    if (!raw) {
                        dateInput.value = "";
                        return;
                    }

                    fp.setDate(raw, true);

                    if (fp.selectedDates.length > 0) {
                        dateInput.value = fp.formatDate(fp.selectedDates[0], "Y-m-d");
                    }
                });
            }

            document.querySelectorAll(".calendar-btn").forEach(btn => {
                btn.addEventListener("click", () => fp.open());
            });

        } catch (e) {
            console.error("flatpickr error:", e);
        }
    }

    // -----------------------------
    // expiration_type の切り替え
    // -----------------------------
    function updateExpiration() {
        const selected = document.querySelector('input[name="expiration_type"]:checked');
        if (!selected) return;

        const isUserInput = selected.value === "2";

        if (dateInput) {
            dateInput.required = isUserInput;
        }

        const wrapper = document.getElementById("date_input_wrapper");
        if (wrapper) {
            wrapper.style.display = isUserInput ? "flex" : "none";
        }
    }

    document.querySelectorAll('input[name="expiration_type"]').forEach(r => {
        r.addEventListener("change", updateExpiration);
    });

    updateExpiration();

    // -----------------------------
    // モーダル表示処理
    // -----------------------------
    try {
        if (window.SHOW_MODAL) {
            const modalEl = document.getElementById("linkModal");
            if (modalEl) {
                const modal = new bootstrap.Modal(modalEl);
                modal.show();
            }
        }
    } catch (e) {
        console.error("Modal error:", e);
    }
});
// ▼ コピー処理
const copyBtn = document.getElementById("copy_btn");
if (copyBtn) {
    copyBtn.addEventListener("click", function () {
        const input = document.getElementById("share_url");
        if (!input) return;

        // クリップボードへコピー
        navigator.clipboard.writeText(input.value).then(() => {

            // ボタンの文字を変更
            copyBtn.textContent = "コピーしました！";

            // ボタンの色も少し変える（任意）
            copyBtn.classList.remove("btn-primary");
            copyBtn.classList.add("btn-success");

            // 2秒後に元に戻す
            setTimeout(() => {
                copyBtn.textContent = "コピー";
                copyBtn.classList.remove("btn-success");
                copyBtn.classList.add("btn-primary");
            }, 2000);

        }).catch(err => {
            console.error("コピー失敗:", err);
            alert("コピーに失敗しました…");
        });
    });
}