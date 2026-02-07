document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".card").forEach(function(card) {

        const checkboxes = card.querySelectorAll("input[type='checkbox']");
        const badge = card.querySelector(".badge");

        updateCount();

        checkboxes.forEach(cb => {
            cb.addEventListener("change", updateCount);
        });

        function updateCount() {
            const total = checkboxes.length;
            const checked = Array.from(checkboxes).filter(cb => cb.checked).length;
            badge.textContent = `${checked} / ${total}`;
        }
    });

});