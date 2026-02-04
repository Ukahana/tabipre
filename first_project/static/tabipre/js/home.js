// タグクリックで複数選択し、即ページ遷移して絞り込み反映
document.querySelectorAll('.tag-badge').forEach(tag => {
    tag.addEventListener('click', function(e) {
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

        // ページ遷移（即反映）
        window.location.search = params.toString();
    });
});
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("keywordInput");

    input.addEventListener("input", function () {
        // 入力が空になったら絞り込み解除
        if (input.value === "") {
            const url = new URL(window.location.href);

            // keyword と page を削除
            url.searchParams.delete("keyword");
            url.searchParams.delete("page");

            window.location.href = url.toString();
        }
    });
});