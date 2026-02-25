document.addEventListener("DOMContentLoaded", function () {

    const dateInput = document.getElementById("id_expiration_date");

    const fp = flatpickr(dateInput, {
        dateFormat: "Y-m-d",
        altInput: true,
        altFormat: "Y/m/d",
        altInputClass: "flatpickr-alt-input",
        allowInput: true,
        locale: "ja",
        clickOpens: false,

        // ★ 旅行編集画面と同じ：年なし日付を補完する
        parseDate: (value, format) => {
            if (!value) return null;

            const nums = value.replace(/[^\d]/g, "");
            const currentYear = new Date().getFullYear();

            // 2/1 → "21"
            if (nums.length === 2) {
                return new Date(currentYear, nums[0] - 1, nums[1]);
            }

            // 3-15 → "315"
            if (nums.length === 3) {
                return new Date(currentYear, nums[0] - 1, nums.slice(1));
            }

            // 0315 → "0315"
            if (nums.length === 4) {
                return new Date(currentYear, nums.slice(0, 2) - 1, nums.slice(2, 4));
            }

            return flatpickr.parseDate(value, format);
        }
    });

    const altInput = fp.altInput;

    // ▼ 手入力 → 本体 input を同期
    altInput.addEventListener("blur", function () {
        const raw = altInput.value.trim();

        if (!raw) {
            dateInput.value = "";
            return;
        }

        // flatpickr にセット（parseDate が補完してくれる）
        fp.setDate(raw, true);

        if (fp.selectedDates.length > 0) {
            dateInput.value = fp.formatDate(fp.selectedDates[0], "Y-m-d");
        }
    });

    // ▼ カレンダーボタン
    document.querySelectorAll(".calendar-btn").forEach(btn => {
        btn.addEventListener("click", () => fp.open());
    });

    // ▼ expiration_type による表示切り替え
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
});