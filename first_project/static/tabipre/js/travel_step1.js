document.addEventListener("DOMContentLoaded", () => {
    const start = document.getElementById("start_date");
    const end = document.getElementById("end_date");
    const stayInfo = document.getElementById("stay_info");
    const nights = document.getElementById("stay_nights");
    const days = document.getElementById("stay_days");
    const stayTypeRadios = document.querySelectorAll("input[name='stay_type']");

    let autoMode = true; // 初期は自動判定モード

    function calcStay() {
        if (!start.value || !end.value) return;

        const s = new Date(start.value);
        const e = new Date(end.value);
        const diff = (e - s) / (1000 * 60 * 60 * 24);

        if (diff >= 0) {
            nights.textContent = `${diff}泊`;
            days.textContent = `${diff + 1}日`;
        }
    }

    function autoDetectStayType() {
        if (!autoMode) return; // 手動変更後は自動判定しない

        if (!start.value || !end.value) return;

        const s = new Date(start.value);
        const e = new Date(end.value);
        const diff = (e - s) / (1000 * 60 * 60 * 24);

        if (diff === 0) {
            // 日帰り
            document.querySelector("input[name='stay_type'][value='daytrip']").checked = true;
            stayInfo.style.display = "none";
        } else if (diff > 0) {
            // 宿泊
            document.querySelector("input[name='stay_type'][value='stay']").checked = true;
            stayInfo.style.display = "block";
            calcStay();
        }
    }

    // 日付変更で自動判定
    start.addEventListener("change", () => {
        autoDetectStayType();
    });
    end.addEventListener("change", () => {
        autoDetectStayType();
    });

    // ユーザーが宿泊タイプを変更したら自動判定を停止
    stayTypeRadios.forEach(radio => {
        radio.addEventListener("change", () => {
            autoMode = false;

            if (radio.value === "stay") {
                stayInfo.style.display = "block";
                calcStay();
            } else {
                stayInfo.style.display = "none";
            }
        });
    });
});