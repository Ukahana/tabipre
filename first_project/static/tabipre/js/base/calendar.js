parseDate: (value, format) => {
    if (!value) return null;

    const nums = value.replace(/[^\d]/g, "");
    const currentYear = new Date().getFullYear();  // ★ 今年の年を取得

    // 4/2 → 今年の 4/2
    if (nums.length === 2) {
        const m = nums[0];
        const d = nums[1];
        return new Date(currentYear, Number(m) - 1, Number(d));
    }

    // 04/02 → 今年の 4/2
    if (nums.length === 4) {
        const m = nums.slice(0, 2);
        const d = nums.slice(2, 4);
        return new Date(currentYear, Number(m) - 1, Number(d));
    }

    return flatpickr.parseDate(value, format);
}