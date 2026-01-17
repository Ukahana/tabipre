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