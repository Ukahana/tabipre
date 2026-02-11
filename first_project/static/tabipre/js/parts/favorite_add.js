document.addEventListener("DOMContentLoaded", () => {

    // ================================
    // ★ モーダルが開いたときに選択をクリア
    // ================================
    const favoriteModal = document.getElementById("favoriteModal");
    if (favoriteModal) {
        favoriteModal.addEventListener("show.bs.modal", () => {
            const checked = document.querySelector(".favorite-radio:checked");
            if (checked) {
                checked.checked = false;
            }
        });
    }

    // ================================
    // ★ お気に入りモーダルの「登録」ボタン
    // ================================
    document.addEventListener("click", (e) => {
        if (e.target.id === "favoriteSelectBtn") {

            const selected = document.querySelector(".favorite-radio:checked");

            // ★ 選択されていない場合は item_name を変更しない
            if (!selected) {
                return;
            }

            const itemInput = document.getElementById("itemNameInput");
            if (itemInput) {
                itemInput.value = selected.value;
            }

            const modalEl = document.getElementById("favoriteModal");
            const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            modal.hide();
        }
    });

    // ================================
    // ★ 星アイコン（favoriteStar）の ON/OFF 切り替え
    // ================================
    const star = document.getElementById("favoriteStar");
    const hidden = document.getElementById("favoriteValue");

    if (star && hidden) {
        star.addEventListener("click", () => {
            const isOn = hidden.value === "1";

            if (isOn) {
                hidden.value = "0";
                star.src = star.dataset.off;
            } else {
                hidden.value = "1";
                star.src = star.dataset.on;
            }
        });
    }

});