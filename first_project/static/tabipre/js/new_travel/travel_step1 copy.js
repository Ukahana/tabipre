document.addEventListener("DOMContentLoaded", function () {

    const startInput = document.getElementById("id_start_date");
    const endInput = document.getElementById("id_end_date");
    const nightsEl = document.getElementById("stay_nights");
    const daysEl = document.getElementById("stay_days");
    const errorEl = document.getElementById("date_error");

    function calcStay() {
        const start = startInput?._flatpickr?.selectedDates[0];
        const end = endInput?._flatpickr?.selectedDates[0];

        nightsEl.textContent = "";
        daysEl.textContent = "";
        errorEl.textContent = "";

        if (!start || !end) return;

        const diff = (end - start) / (1000 * 60 * 60 * 24);

        if (diff < 0) {
            errorEl.textContent = "終了日は開始日より後の日付を選択してください";
            return;
        }

        nightsEl.textContent = diff;
        daysEl.textContent = diff + 1;
    }

    // ▼ flatpickr 初期化（年なし日付対応）
    document.querySelectorAll(".calendar-btn").forEach(btn => {
        const targetId = btn.dataset.target;
        const input = document.getElementById(targetId);
        if (!input) return;

        flatpickr(input, {
            dateFormat: "Y-m-d",
            altInput: true,
            altFormat: "Y/m/d",
            allowInput: true,
            locale: "ja",
            clickOpens: false,
            onChange: calcStay,

            // ★ 年なし日付を補完（
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

        // ▼ カレンダーボタン
        btn.addEventListener("click", () => input._flatpickr.open());

        // ▼ 手入力 → flatpickr に反映 → calcStay 発動
        input.addEventListener("change", () => {
            if (input._flatpickr) {
                input._flatpickr.setDate(input.value, true);
            }
        });
    });

    calcStay();
});