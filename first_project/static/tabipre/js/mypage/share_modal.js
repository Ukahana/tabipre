document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("shareLinkModal");

    modal.addEventListener("show.bs.modal", function (event) {
        const trigger = event.relatedTarget;

        const linkId = trigger.getAttribute("data-link-id");
        const url = trigger.getAttribute("data-url");
        const permission = trigger.getAttribute("data-permission");

        document.getElementById("share-url").value = url;

        document.getElementById("perm-view").checked = permission === "view";
        document.getElementById("perm-edit").checked = permission === "edit";

        document.getElementById("delete-link").href = `/share/${linkId}/delete/`;

        document.getElementById("save-btn").onclick = () => {
            const selected = document.querySelector("input[name='permission']:checked").value;

            fetch(`/share/${linkId}/update/`, {
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
    });

    // コピー機能
    document.getElementById("copy-btn").onclick = () => {
        const input = document.getElementById("share-url");
        input.select();
        navigator.clipboard.writeText(input.value);
    };
});
