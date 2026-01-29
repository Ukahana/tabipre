document.addEventListener("DOMContentLoaded", function () {
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

        btn.addEventListener("click", () => fp.open());
    });
});