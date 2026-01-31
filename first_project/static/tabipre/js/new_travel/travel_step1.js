document.addEventListener("DOMContentLoaded", function () {

    // -----------------------------
    // flatpickr 初期化（カレンダーアイコン対応）
    // -----------------------------
    document.querySelectorAll(".calendar-btn").forEach(btn => {
        const targetId = btn.dataset.target;
        const input = document.getElementById(targetId);

        if (!input) return;

        const fp = flatpickr(input, {
            dateFormat: "Y.m.d",
            altInput: true,
            altFormat: "Y/m/d",
            allowInput: true,
            locale: "ja",
            clickOpens: false,

            // 手入力・カレンダー選択どちらでも泊数計算
            onChange: calcStay,

            // 数字だけ入力されたときの補正
            parseDate: (value, format) => {
                if (!value) return null;

                const nums = value.replace(/[^\d]/g, "");
                const currentYear = new Date().getFullYear();

                if (nums.length === 2) {
                    const m = nums[0];
                    const d = nums[1];
                    return new Date(currentYear, Number(m) - 1, Number(d));
                }

                if (nums.length === 4) {
                    const m = nums.slice(0, 2);
                    const d = nums.slice(2, 4);
                    return new Date(currentYear, Number(m) - 1, Number(d));
                }

                return flatpickr.parseDate(value, format);
            }
        });

        // 📅 ボタンでカレンダーを開く
        btn.addEventListener("click", () => fp.open());
    });


    // -----------------------------
    // 何泊何日 計算
    // -----------------------------
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

    // 入力変更時にも計算
    startInput?.addEventListener("change", calcStay);
    endInput?.addEventListener("change", calcStay);

    // 初期表示でも泊数を計算
    calcStay();
});