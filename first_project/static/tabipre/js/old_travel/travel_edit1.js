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

        if (!start || !end) return;

        const diff = (end - start) / (1000 * 60 * 60 * 24);

        if (diff < 0) {
            errorEl.textContent = "終了日は開始日より後の日付を選択してください";
            return;
        }

        nightsEl.textContent = diff;
        daysEl.textContent = diff + 1;
    }

    document.querySelectorAll(".date-wrapper input").forEach(input => {

        if (input._flatpickr) return;

        const fp = flatpickr(input, {
            dateFormat: "Y-m-d",
            allowInput: false,  
            locale: "ja",
            clickOpens: true,
            onChange: calcStay,
            onValueUpdate: calcStay,
        });

        if (input.id === "id_start_date") startFP = fp;
        if (input.id === "id_end_date") endFP = fp;
    });

    calcStay();
});