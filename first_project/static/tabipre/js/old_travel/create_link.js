document.addEventListener("DOMContentLoaded", function () {
    const dateInput = document.getElementById("id_expiration_date");
    const openCalendarBtn = document.getElementById("open_calendar_btn");

    // ▼ USER_INPUT（= value "2"）のときだけ required にする
    //    ＋ 自動計算タイプなら日付を自動セット
    function updateExpiration() {
        const selected = document.querySelector('input[name="expiration_type"]:checked');
        if (!selected) return;

        const isUserInput = selected.value === "2";
        dateInput.required = isUserInput;

        // ▼ 自動計算タイプなら日付を自動セット
        const autoDate = selected.dataset.expirationDate;
        if (!isUserInput && autoDate) {
            dateInput.value = autoDate;
        }
    }

    document.querySelectorAll('input[name="expiration_type"]').forEach(r => {
        r.addEventListener("change", updateExpiration);
    });

    updateExpiration();  // 初期状態でも反映


    // ▼ カレンダーアイコン → 一時的に type="date" にして picker を開く
    if (openCalendarBtn) {
        openCalendarBtn.addEventListener("click", function () {
            dateInput.type = "date";
            dateInput.showPicker?.();

            dateInput.addEventListener("blur", function handler() {
                dateInput.type = "text";
                dateInput.removeEventListener("blur", handler);
            });
        });
    }

    // ▼ 手入力 or カレンダー選択後に YYYY-MM-DD に統一
    dateInput.addEventListener("change", function () {
        const raw = dateInput.value.trim();
        if (!raw) return;

        const normalized = raw.replace(/[\/\.]/g, "-");
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

            const yyyy = date.getFullYear();
            const mm = String(date.getMonth() + 1).padStart(2, "0");
            const dd = String(date.getDate()).padStart(2, "0");

            dateInput.value = `${yyyy}-${mm}-${dd}`;

        } catch (e) {
            alert("正しい日付を入力してください（例: 2/5）");
            dateInput.value = "";
        }
    });
});