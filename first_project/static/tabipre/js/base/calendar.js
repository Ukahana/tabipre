parseDate: (value, format) => {
    if (!value) return null;

    // 数字以外を除去
    const nums = value.replace(/[^\d]/g, "");

    // 入力禁止なので、4桁以外は flatpickr に任せる
    if (nums.length !== 8) {
        return flatpickr.parseDate(value, format);
    }

    // YYYYMMDD の場合のみ処理
    const y = Number(nums.slice(0, 4));
    const m = Number(nums.slice(4, 6));
    const d = Number(nums.slice(6, 8));

    if (m >= 1 && m <= 12 && d >= 1 && d <= 31) {
        return new Date(y, m - 1, d);
    }

    // それ以外は flatpickr 標準
    return flatpickr.parseDate(value, format);
}