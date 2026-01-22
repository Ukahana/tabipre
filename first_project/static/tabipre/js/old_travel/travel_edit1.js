document.addEventListener("DOMContentLoaded", function () {
    const startInput = document.getElementById("id_start_date");
    const endInput = document.getElementById("id_end_date");
    const nightsSpan = document.getElementById("stay_nights");
    const daysSpan = document.getElementById("stay_days");
    const errorBox = document.getElementById("date_error");
    const stayInfo = document.getElementById("stay_info");

    function updateStay() {
        const startValue = startInput.value;
        const endValue = endInput.value;

        // 入力が揃っていない場合
        if (!startValue || !endValue) {
            nightsSpan.textContent = "-";
            daysSpan.textContent = "-";
            errorBox.textContent = "";
            stayInfo.style.visibility = "hidden";
            return;
        }

        const start = new Date(startValue);
        const end = new Date(endValue);

        // 日付が逆の場合
        if (end < start) {
            errorBox.textContent = "終了日は開始日より後の日付を選択してください。";
            nightsSpan.textContent = "-";
            daysSpan.textContent = "-";
            stayInfo.style.visibility = "hidden";
            return;
        }

        errorBox.textContent = "";

        // 泊数・日数計算
        const diff = Math.round((end - start) / (1000 * 60 * 60 * 24));
        nightsSpan.textContent = diff;
        daysSpan.textContent = diff + 1;

        // 常に表示
        stayInfo.style.visibility = "visible";
    }

    startInput.addEventListener("change", updateStay);
    endInput.addEventListener("change", updateStay);

    updateStay();
});