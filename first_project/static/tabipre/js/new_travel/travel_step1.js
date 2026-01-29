document.addEventListener("DOMContentLoaded", () => {
    const start = document.getElementById("id_start_date");
    const end = document.getElementById("id_end_date");
    const stayInfo = document.getElementById("stay_info");
    const nights = document.getElementById("stay_nights");
    const days = document.getElementById("stay_days");
    const stayTypeRadios = document.querySelectorAll("input[name='stay_type']");

    let autoMode = true;

    // ★ Flatpickr の "Y.m.d" を Date に変換する関数
    function parseYmd(str) {
        if (!str) return null;
        const parts = str.split(".");
        if (parts.length !== 3) return null;
        return new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
    }

    function calcStay() {
        if (!start.value || !end.value) return;

        const s = parseYmd(start.value);
        const e = parseYmd(end.value);
        if (!s || !e) return;

        const diff = Math.round((e - s) / (1000 * 60 * 60 * 24));

        if (diff >= 0) {
            nights.textContent = diff;
            days.textContent = diff + 1;
        }
    }

    function autoDetectStayType() {
        if (!autoMode) return;
        if (!start.value || !end.value) return;

        const s = parseYmd(start.value);
        const e = parseYmd(end.value);
        if (!s || !e) return;

        const diff = Math.round((e - s) / (1000 * 60 * 60 * 24));

        if (diff === 0) {
            document.querySelector("input[name='stay_type'][value='0']").checked = true;
            stayInfo.style.display = "none";
        } else if (diff > 0) {
            document.querySelector("input[name='stay_type'][value='1']").checked = true;
            stayInfo.style.display = "block";
            calcStay();
        }
    }

    start.addEventListener("change", autoDetectStayType);
    end.addEventListener("change", autoDetectStayType);

    stayTypeRadios.forEach(radio => {
        radio.addEventListener("change", () => {
            autoMode = false;

            if (radio.value === "0") {
                stayInfo.style.display = "none";
                calcStay();
            } else if (radio.value === "1") {
                stayInfo.style.display = "block";
                calcStay();
            }
        });
    });

    // 初期状態反映
    autoDetectStayType();
});