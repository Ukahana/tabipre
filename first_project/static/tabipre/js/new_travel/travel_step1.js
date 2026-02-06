function initTravelForm() {

    // -----------------------------
    // flatpickr 初期化
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
            onChange: calcStay,
        });

        btn.addEventListener("click", () => fp.open());
    });

    // -----------------------------
    // 泊数計算
    // -----------------------------
    const startInput = document.getElementById("id_start_date");
    const endInput = document.getElementById("id_end_date");

    const nightsEl = document.getElementById("stay_nights");
    const daysEl = document.getElementById("stay_days");

    function calcStay() {
        const start = startInput?._flatpickr?.selectedDates[0];
        const end = endInput?._flatpickr?.selectedDates[0];

        // 初期化
        nightsEl.textContent = "";
        daysEl.textContent = "";

        // どちらか未入力なら終了
        if (!start || !end) return;

        const diff = (end - start) / (1000 * 60 * 60 * 24);

        // マイナス泊数は表示しない
        if (diff < 0) return;

        nightsEl.textContent = diff;
        daysEl.textContent = diff + 1;
    }

    // 入力変更時に再計算
    startInput?.addEventListener("change", calcStay);
    endInput?.addEventListener("change", calcStay);

    // 初期表示でも計算
    calcStay();
}

// ページ読み込み時に実行
document.addEventListener("DOMContentLoaded", initTravelForm);