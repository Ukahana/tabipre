document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("shareLinkModal");
    let currentLinkId = null;

    // モーダル表示時
    modal.addEventListener("show.bs.modal", function (event) {
        const trigger = event.relatedTarget;

        currentLinkId = trigger.getAttribute("data-link-id");
        const url = trigger.getAttribute("data-url");
        const permission = trigger.getAttribute("data-permission");
        const expiration = trigger.getAttribute("data-expiration");

        document.getElementById("share-url").value = url;

        document.getElementById("perm-view").checked = permission === "0";
        document.getElementById("perm-edit").checked = permission === "1";

        const expInput = document.getElementById("share-expiration");
        if (expInput) expInput.value = expiration;

        // メッセージを初期化
        document.getElementById("copy-msg").textContent = "";
    });

    // 🔥 リンク削除
    document.getElementById("delete-link").onclick = (e) => {
        e.preventDefault();

        const form = document.getElementById("delete-link-form");
        form.action = `/share/${currentLinkId}/delete/`;

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

    // 🔵 保存処理
    document.getElementById("save-btn").onclick = () => {
        const selected = document.querySelector("input[name='permission']:checked").value;

        fetch(`/share/${currentLinkId}/update/`, {
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

    // 📋 コピー機能（JSだけでメッセージ表示）
    document.getElementById("copy-btn").onclick = () => {
        const input = document.getElementById("share-url");
        const msg = document.getElementById("copy-msg");

        navigator.clipboard.writeText(input.value).then(() => {

            msg.textContent = "コピーしました";

            // 1.5秒後に消す
            setTimeout(() => {
                msg.textContent = "";
            }, 1500);
        });
    };
});