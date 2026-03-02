document.addEventListener("DOMContentLoaded", function () {

    // -----------------------------
    // その他の表示切替
    // -----------------------------
    const otherCheckbox = document.querySelector('.transport-other input[type="checkbox"]');
    const otherBox = document.querySelector('.transport-other-box');

    if (otherCheckbox && otherBox) {
        const toggle = () => {
            otherBox.style.display = otherCheckbox.checked ? "inline-block" : "none";
        };
        otherCheckbox.addEventListener("change", toggle);
        toggle();
    }

});