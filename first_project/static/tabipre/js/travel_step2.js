console.log("読み込まれた")
document.addEventListener("DOMContentLoaded", function () {
    const otherCheckbox = document.querySelector('#id_transport_types_5');
    const otherBox = document.querySelector('.transport-other-box');

    if (!otherCheckbox || !otherBox) return;

    function toggleOtherBox() {
        otherBox.style.display = otherCheckbox.checked ? "inline-block" : "none";
    }

    otherCheckbox.addEventListener("change", toggleOtherBox);
    toggleOtherBox(); // 初期状態反映
});