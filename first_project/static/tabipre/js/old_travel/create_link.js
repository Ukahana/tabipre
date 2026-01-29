document.addEventListener("DOMContentLoaded", function () {

    const dateInput = document.getElementById("id_expiration_date");
    const openCalendarBtn = document.getElementById("open_calendar_btn");

    // ▼ USER_INPUT（= value "2"）のときだけ required にする
    function updateExpiration() {
        const selected = document.querySelector('input[name="expiration_type"]:checked');
        if (!selected) return;

        const isUserInput = selected.value === "2";
        dateInput.required = isUserInput;
    }

    document.querySelectorAll('input[name="expiration_type"]').forEach(r => {
        r.addEventListener("change", updateExpiration);
    });

    updateExpiration();  // 初期状態でも反映


    // ▼ 手入力したときのフォーマット統一
    dateInput.addEventListener("change", function () {
        const raw = dateInput.value.trim();
        if (!raw) return;

        const normalized = raw.replace(/[\/\.]/g, "-").replace(/\s+/g, "");
        const parts = normalized.split("-");

        let year, month, day;

        try {
            if (parts.length === 3) {
                [year, month, day] = parts;
            } else if (parts.length === 2) {
                year = new Date().getFullYear();
                [month, day] = parts;
            } else {
                throw new Error("invalid");
            }

            const date = new Date(year, month - 1, day);
            if (isNaN(date.getTime())) throw new Error("invalid");

            dateInput.value = `${date.getFullYear()}.${date.getMonth() + 1}.${date.getDate()}`;

        } catch (e) {
            alert("正しい日付を入力してください（例: 2/5）");
            dateInput.value = "";
        }
    });

});