document.addEventListener("DOMContentLoaded", function () {
    const startInput = document.getElementById("id_start_date");
    const endInput = document.getElementById("id_end_date");
    const nightsSpan = document.getElementById("stay_nights");
    const daysSpan = document.getElementById("stay_days");
    const errorBox = document.getElementById("date_error");

    function updateStay() {
        const start = new Date(startInput.value);
        const end = new Date(endInput.value);

        if (!isNaN(start) && !isNaN(end)) {

            if (end < start) {
                errorBox.textContent = "終了日は開始日より後の日付を選択してください。";
                nightsSpan.textContent = "-";
                daysSpan.textContent = "-";
                return;
            }

            errorBox.textContent = "";
            const diff = (end - start) / (1000 * 60 * 60 * 24);
            nightsSpan.textContent = diff + "泊";
            daysSpan.textContent = (diff + 1) + "日";
        }
    }

    startInput.addEventListener("change", updateStay);
    endInput.addEventListener("change", updateStay);
});
