document.addEventListener("DOMContentLoaded", function () {

    let startFP, endFP;

    const nightsEl = document.getElementById("stay_nights");
    const daysEl = document.getElementById("stay_days");
    const errorEl = document.getElementById("date_error");

    function calcStay() {
        const start = startFP?.selectedDates[0];
        const end = endFP?.selectedDates[0];

        nightsEl.textContent = "";
        daysEl.textContent = "";
        errorEl.textContent = "";

        errorEl.textContent = "";

        if (!start || !end) return;

        const diff = (end - start) / (1000 * 60 * 60 * 24);

        if (diff < 0) {
            return;
        }

        nightsEl.textContent = diff;
        daysEl.textContent = diff + 1;
    }

    const commonOptions = {
        dateFormat: "Y-m-d",
        altInput: true,
        altFormat: "Y/m/d",
        allowInput: false,
        locale: "ja",
        disableMobile: true,
        clickOpens: true,
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
    };

    // ▼ .date-wrapper 内の input を flatpickr 化
    document.querySelectorAll(".date-wrapper input").forEach(input => {

        if (input._flatpickr) return;

        const fp = flatpickr(input, commonOptions);

        if (input.id === "id_start_date") startFP = fp;
        if (input.id === "id_end_date") endFP = fp;
    });

    calcStay();
});