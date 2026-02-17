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

    document.querySelectorAll(".calendar-btn").forEach(btn => {
        const targetId = btn.dataset.target;
        const input = document.getElementById(targetId);
        if (!input) return;

        flatpickr(input, {
            dateFormat: "Y.m.d",
            altInput: true,
            altFormat: "Y/m/d",
            allowInput: true,
            locale: "ja",
            clickOpens: false,
            onChange: calcStay,
        });

        btn.addEventListener("click", () => input._flatpickr.open());

        // 手入力 → flatpickr に反映 → calcStay 発動
        input.addEventListener("change", () => {
            if (input._flatpickr) {
                input._flatpickr.setDate(input.value, true);
            }
        });
    });

    calcStay();
});