document.addEventListener("DOMContentLoaded", function () {

    const dateInput = document.getElementById("id_expiration_date");

    const fp = flatpickr(dateInput, {
        dateFormat: "Y-m-d",          // Django に送る形式
        altInput: true,
        altFormat: "Y/m/d",           // 表示用
        altInputClass: "flatpickr-alt-input",
        allowInput: true,
        locale: "ja",
        clickOpens: false,
    });

    const altInput = fp.altInput;

    // ★ 手入力 → 本体 input を確実に同期
    altInput.addEventListener("blur", function () {
        const raw = altInput.value.trim();

        if (!raw) {
            dateInput.value = "";
            return;
        }

        // flatpickr 標準パーサーに任せる
        fp.setDate(raw, true);

        // 本体 input を YYYY-MM-DD で更新
        if (fp.selectedDates.length > 0) {
            dateInput.value = fp.formatDate(fp.selectedDates[0], "Y-m-d");
        }
    });

    // カレンダーボタン
    document.querySelectorAll(".calendar-btn").forEach(btn => {
        btn.addEventListener("click", () => fp.open());
    });

    // expiration_type による表示切り替え
    function updateExpiration() {
        const selected = document.querySelector('input[name="expiration_type"]:checked');
        if (!selected) return;

        const isUserInput = selected.value === "2";
        dateInput.required = isUserInput;

        const wrapper = document.getElementById("date_input_wrapper");
        wrapper.style.display = isUserInput ? "flex" : "none";
    }

    document.querySelectorAll('input[name="expiration_type"]').forEach(r => {
        r.addEventListener("change", updateExpiration);
    });

    updateExpiration();

    // モーダル
    if (window.SHOW_MODAL === true) {
        const modalEl = document.getElementById("linkModal");
        if (modalEl) {
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
        }
    }
});