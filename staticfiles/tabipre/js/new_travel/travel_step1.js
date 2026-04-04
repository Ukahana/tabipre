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

        // 終了日 < 開始日 のときは計算しない
        if (diff < 0) {
            return;
        }

        nightsEl.textContent = diff;
        daysEl.textContent = diff + 1;
    }

    // ▼ start_date の flatpickr
    flatpickr(startInput, {
        dateFormat: "Y-m-d",
        altInput: true,
        altFormat: "Y/m/d",
        allowInput: false,
        locale: "ja",
        disableMobile: true,
        minDate: "today",
        onChange: calcStay,
        parseDate: (value, format) => {
            if (!value) return null;

            const nums = value.replace(/[^\d]/g, "");
            const currentYear = new Date().getFullYear();

            if (nums.length === 2) return new Date(currentYear, nums[0] - 1, nums[1]);
            if (nums.length === 3) return new Date(currentYear, nums[0] - 1, nums.slice(1));
            if (nums.length === 4) return new Date(currentYear, nums.slice(0, 2) - 1, nums.slice(2, 4));

            return flatpickr.parseDate(value, format);
        }
    });

    // ▼ end_date の flatpickr
    flatpickr(endInput, {

        dateFormat: "Y-m-d",
        altInput: true,
        altFormat: "Y/m/d",
        allowInput: false,
        locale: "ja",
        disableMobile: true,
        minDate: "today",
        onChange: calcStay,
        parseDate: (value, format) => {
            if (!value) return null;

            const nums = value.replace(/[^\d]/g, "");
            const currentYear = new Date().getFullYear();

            if (nums.length === 2) return new Date(currentYear, nums[0] - 1, nums[1]);
            if (nums.length === 3) return new Date(currentYear, nums[0] - 1, nums.slice(1));
            if (nums.length === 4) return new Date(currentYear, nums.slice(0, 2) - 1, nums.slice(2, 4));

            return flatpickr.parseDate(value, format);
        }
    });

    calcStay();
});