document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("shareLinkModal");

    let currentToken = null;

    // モーダル表示時
    modal.addEventListener("show.bs.modal", function (event) {
        const trigger = event.relatedTarget;

        currentToken = trigger.getAttribute("data-token");

        const url = trigger.getAttribute("data-url");
        const permission = trigger.getAttribute("data-permission");
        const expiration = trigger.getAttribute("data-expiration");

        // URL をセット
        document.getElementById("share-url").value = url;

        // 権限ラジオ（0/1 どちらでも判定できるように）
        document.getElementById("perm-view").checked = (permission == 0 || permission == "0");
        document.getElementById("perm-edit").checked = (permission == 1 || permission == "1");

        // 有効期限（もしあれば）
        const expInput = document.getElementById("share-expiration");
        if (expInput) expInput.value = expiration;

        // コピー完了メッセージ初期化
        document.getElementById("copy-msg").textContent = "";
    });

    // 🔥 リンク削除
    document.getElementById("delete-link").onclick = (e) => {
        e.preventDefault();

        const form = document.getElementById("delete-link-form");

        // ★ token ベースの URL（/tabipre/ を忘れない）
        form.action = `/tabipre/share/${currentToken}/delete/`;

        const shareModal = bootstrap.Modal.getInstance(modal);
        shareModal.hide();

        modal.addEventListener(
            "hidden.bs.modal",
            () => {
                const deleteModal = new bootstrap.Modal(document.getElementById("deleteLinkModal"));
                deleteModal.show();
            },
            { once: true }
        );
    };

    // 🔵 保存処理（権限変更）
    document.getElementById("save-btn").onclick = () => {
        const selected = document.querySelector("input[name='permission']:checked").value;

        // ★ token ベースの URL（/tabipre/ を忘れない）
        fetch(`/tabipre/share/${currentToken}/update/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ permission: selected })
        }).then(() => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            modalInstance.hide();
            location.reload();
        });
    };

    // 📋 コピー機能
    document.getElementById("copy-btn").onclick = () => {
        const input = document.getElementById("share-url");
        const msg = document.getElementById("copy-msg");

        navigator.clipboard.writeText(input.value).then(() => {
            msg.textContent = "コピーしました";

            setTimeout(() => {
                msg.textContent = "";
            }, 1500);
        });
    };
});