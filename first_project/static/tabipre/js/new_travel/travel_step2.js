document.addEventListener("DOMContentLoaded", function () {
    const checkboxes = document.querySelectorAll('input[name="transport_types"]');
    const otherBox = document.querySelector('.transport-other-box');

    if (!checkboxes.length || !otherBox) return;

    function toggleOtherBox() {
        const isChecked = [...checkboxes].some(cb => cb.checked && cb.value === "OTHER");
        otherBox.style.display = isChecked ? "inline-block" : "none";
    }

    checkboxes.forEach(cb => cb.addEventListener("change", toggleOtherBox));
    toggleOtherBox(); // 初期状態反映
});