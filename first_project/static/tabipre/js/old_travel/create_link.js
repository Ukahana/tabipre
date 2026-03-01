document.addEventListener("DOMContentLoaded", function () {

    // -----------------------------
    // 日付入力（flatpickr）
    // -----------------------------
    const dateInput = document.getElementById("id_expiration_date");

    let fp = null;

    if (dateInput) {
        try {
            fp = flatpickr(dateInput, {
                dateFormat: "Y-m-d",
                altInput: true,
                altFormat: "Y/m/d",
                altInputClass: "flatpickr-alt-input",
                allowInput: false,      // ← 手入力禁止
                locale: "ja",
                clickOpens: true,       // ← 入力欄クリックでカレンダーを開く
                minDate: "today",
                disableMobile: true       // ← 過去日を選べない
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
            wrapper.style.display = isUserInput ? "block" : "none";
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

        navigator.clipboard.writeText(input.value).then(() => {

            copyBtn.textContent = "コピーしました！";
            copyBtn.classList.remove("btn-primary");
            copyBtn.classList.add("btn-success");

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