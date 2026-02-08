document.addEventListener("DOMContentLoaded", function () {

    const dateInput = document.getElementById("id_expiration_date");

    const fp = flatpickr(dateInput, {
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
                return new Date(currentYear, nums[0] - 1, nums[1]);
            }
            if (nums.length === 4) {
                return new Date(currentYear, nums.slice(0, 2) - 1, nums.slice(2, 4));
            }
            if (nums.length === 6) {
                return new Date(nums.slice(0, 4), nums.slice(4, 6) - 1, nums.slice(6, 8));
            }
            if (nums.length === 8) {
                return new Date(nums.slice(0, 4), nums.slice(4, 6) - 1, nums.slice(6, 8));
            }

            return null;
        }
    });

    const altInput = fp.altInput;

    altInput.addEventListener("blur", function () {
        const raw = altInput.value.trim();
        if (!raw) {
            dateInput.value = "";
            return;
        }
        fp.setDate(raw, true);
    });

    document.querySelectorAll(".calendar-btn").forEach(btn => {
        btn.addEventListener("click", () => fp.open());
    });

    function updateExpiration() {
        const selected = document.querySelector('input[name="expiration_type"]:checked');
        if (!selected) return;

        const isUserInput = selected.value === "2";
        dateInput.required = isUserInput;

        const wrapper = document.getElementById("date_input_wrapper");
        wrapper.style.display = isUserInput ? "flex" : "none";
    }

    document.querySelectorAll('input[name="expiration_type"]').forEach(r => {
        r.addEventListener("change", updateExpiration);
    });

    updateExpiration();

    // ★ モーダルを開く処理（SHOW_MODAL がテンプレートから渡される）
    if (window.SHOW_MODAL === true) {
        const modalEl = document.getElementById("linkModal");
        if (modalEl) {
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
        }
    }
});