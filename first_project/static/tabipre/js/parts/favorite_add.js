// お気に入りモーダルの「登録」ボタンが押されたとき
document.addEventListener("click", (e) => {

  if (e.target.id === "favoriteSelectBtn") {

    // 選択されたお気に入り項目
    const selected = document.querySelector(".favorite-radio:checked");
    if (!selected) return;

    // ★ この画面は itemNameInput に直接セットするだけでOK
    const itemInput = document.getElementById("itemNameInput");
    if (itemInput) {
      itemInput.value = selected.value;
    }

    // モーダルを閉じる
    const modalEl = document.getElementById("favoriteModal");
    const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
    modal.hide();
  }
});