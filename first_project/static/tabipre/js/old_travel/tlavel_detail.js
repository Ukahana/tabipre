// CSRFトークン取得（Django標準）
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// チェック処理（画面を動かさない）
function toggleItem(checkbox, itemId) {
    const checked = checkbox.checked;
    const currentPos = window.scrollY;

    fetch(`/toggle_item/${itemId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ checked: checked })
    }).then(() => {
        window.scrollTo(0, currentPos);
    });
}