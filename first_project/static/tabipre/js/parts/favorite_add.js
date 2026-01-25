document.addEventListener("click", (e) => {

  // favoriteSelectBtn がクリックされたときだけ反応
  if (e.target.id === "favoriteSelectBtn") {

    const selected = document.querySelector(".favorite-radio:checked");
    if (!selected) return;

    // どの項目に追加するか
    const targetId = e.target.dataset.targetId;
    const itemInput = document.getElementById("item_" + targetId);

    if (itemInput) {
      itemInput.value = selected.value;

      // localStorage 保存
      const STORAGE_KEY = "template_edit_temp_" + itemInput.dataset.templateId;
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
      saved[itemInput.name] = selected.value;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(saved));
    }

    // モーダル閉じる
    const modalEl = document.getElementById("favoriteModal");
    const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
    modal.hide();
  }
});