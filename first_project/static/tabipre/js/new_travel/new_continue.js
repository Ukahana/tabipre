function submitCategoryForm(action) {
    const form = document.getElementById('categoryItemForm');

    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = action;
    input.value = '1';
    form.appendChild(input);

    form.submit();
}