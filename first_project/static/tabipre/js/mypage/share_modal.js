document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("shareLinkModal");

    let currentLinkId = null;

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
    });

    // 🔥 削除リンク（show.bs.modal の外で設定）
    document.getElementById("delete-link").onclick = (e) => {
        e.preventDefault();

        const form = document.getElementById("delete-link-form");
        form.action = `/share/${currentLinkId}/delete/`;

        const shareModal = bootstrap.Modal.getInstance(document.getElementById("shareLinkModal"));
        shareModal.hide();

        document.getElementById("shareLinkModal").addEventListener(
            "hidden.bs.modal",
            () => {
                const deleteModal = new bootstrap.Modal(document.getElementById("deleteLinkModal"));
                deleteModal.show();
            },
            { once: true }
        );
    };

    // 保存
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

    // コピー機能
    document.getElementById("copy-btn").onclick = () => {
        const input = document.getElementById("share-url");
        input.select();
        navigator.clipboard.writeText(input.value);
    };
});