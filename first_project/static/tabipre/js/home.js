// ===============================
// タグクリックで複数選択し、即ページ遷移
// ===============================
document.querySelectorAll('.tag-badge').forEach(tag => {
    tag.addEventListener('click', function (e) {
        e.preventDefault();

        const type = this.dataset.type;      // travel_type or transport
        const value = this.dataset.value;    // "0", "1", "2"...

        const params = new URLSearchParams(window.location.search);

        // 現在の選択値を配列で取得
        let selected = params.getAll(type);

        if (selected.includes(value)) {
            // すでに選択されている → 削除
            selected = selected.filter(v => v !== value);
        } else {
            // 選択されていない → 追加
            selected.push(value);
        }

        // 一旦削除してから複数追加
        params.delete(type);
        selected.forEach(v => params.append(type, v));

        // ページ番号はリセット
        params.delete("page");

        // ページ遷移（即反映）
        window.location.search = params.toString();
    });
});


// ===============================
// キーワード入力欄のクリアで絞り込み解除
// ===============================
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("keywordInput");
    const clearBtn = document.getElementById("clearBtn");

    // 入力時に × ボタン表示
    input.addEventListener("input", function () {
        clearBtn.style.display = input.value ? "block" : "none";

        if (input.value === "") {
            const url = new URL(window.location.href);
            url.searchParams.delete("keyword");
            url.searchParams.delete("page");
            url.searchParams.delete("travel_type");
            url.searchParams.delete("transport");
            url.searchParams.delete("sort");
            window.location.href = url.toString();
        }
    });

    // × ボタン押下でクリア
    clearBtn.addEventListener("click", function () {
        input.value = "";
        clearBtn.style.display = "none";

        const url = new URL(window.location.href);
        url.searchParams.delete("keyword");
        url.searchParams.delete("page");
        url.searchParams.delete("travel_type");
        url.searchParams.delete("transport");
        url.searchParams.delete("sort");
        window.location.href = url.toString();
    });
});