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
    const dateInput = document.getElementById("id_expiration_date");

    if (type === "2") {
      dateInputWrapper.style.display = "block";
      dateInput.required = true;
    } else {
      dateInputWrapper.style.display = "none";
      dateInput.required = false;
    }
  }

  document.querySelectorAll('input[name="expiration_type"]').forEach(r => {
    r.addEventListener("change", updateExpiration);
  });

  updateLabels();
  updateExpiration();

  // ★ モーダル処理
  if (window.SHOW_MODAL) {
    const modalEl = document.getElementById("createdModal");
    if (modalEl) {
      const modal = new bootstrap.Modal(modalEl);
      modal.show();

      const copyBtn = document.getElementById("copy_btn");
      if (copyBtn) {
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
    }
  }
};