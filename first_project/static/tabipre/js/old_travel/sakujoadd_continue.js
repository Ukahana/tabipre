document.addEventListener("DOMContentLoaded", function() {
    const star = document.getElementById("favoriteStar");
    const hidden = document.getElementById("favoriteValue");

    star.addEventListener("click", function() {
        const isOn = hidden.value === "1";

        if (isOn) {
            star.src = star.dataset.off;
            hidden.value = "0";
        } else {
            star.src = star.dataset.on;
            hidden.value = "1";
        }
    });
});