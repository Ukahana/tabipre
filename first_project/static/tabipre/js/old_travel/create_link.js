window.onload = function () {
  const labelOneMonth = document.getElementById("label_one_month");
  const labelAfterTrip = document.getElementById("label_after_trip");
  const dateInputWrapper = document.getElementById("date_input_wrapper");

  function updateLabels() {
    const now = new Date();
    const oneMonthLater = new Date(now);
    oneMonthLater.setMonth(now.getMonth() + 1);
    labelOneMonth.textContent =
      `${oneMonthLater.getFullYear()}/${oneMonthLater.getMonth() + 1}/${oneMonthLater.getDate()}まで`;

    const tripEnd = document.getElementById("trip_end_date")?.value;
    labelAfterTrip.textContent = tripEnd ? `${tripEnd}まで` : "取得できません";
  }

  function updateExpiration() {
    const type = document.querySelector('input[name="expiration_type"]:checked')?.value;
    dateInputWrapper.style.display = type === "2" ? "block" : "none";
  }

  document.querySelectorAll('input[name="expiration_type"]').forEach(r => {
    r.addEventListener("change", updateExpiration);
  });

  updateLabels();
  updateExpiration();

  // ★ モーダル処理（window.onload 内で直接実行）
  if (window.SHOW_MODAL) {
    const modal = new bootstrap.Modal(document.getElementById("createdModal"));
    modal.show();

    const copyBtn = document.getElementById("copy_btn");
    copyBtn.addEventListener("click", async function () {
      const input = document.getElementById("share_url");
      try {
        await navigator.clipboard.writeText(input.value);
        alert("コピーしました");
      } catch (err) {
        alert("コピーに失敗しました");
      }
    });
  }
};