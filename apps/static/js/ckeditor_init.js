// Инициализация CKEditor для текстовых полей
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация для полей content новостей
    const textareaIds = [
        'id_content',
        'id_content_uz',
        'id_content_ru',
        'id_content_en',
        'id_text_content',
        'id_text_content_uz',
        'id_text_content_ru',
        'id_text_content_en'
    ];
    
    textareaIds.forEach(function(id) {
        const textarea = document.getElementById(id);
        if (textarea) {
            CKEDITOR.replace(id, {
                height: 400,
                toolbar: [
                    { name: 'document', items: [ 'Source', '-', 'NewPage', 'Preview', '-', 'Templates' ] },
                    { name: 'clipboard', items: [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo' ] },
                    { name: 'editing', items: [ 'Find', 'Replace', '-', 'SelectAll' ] },
                    '/',
                    { name: 'basicstyles', items: [ 'Bold', 'Italic', 'Underline', 'Strike', '-', 'RemoveFormat' ] },
                    { name: 'paragraph', items: [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote' ] },
                    { name: 'links', items: [ 'Link', 'Unlink' ] },
                    { name: 'insert', items: [ 'Image', 'Table', 'HorizontalRule' ] },
                    '/',
                    { name: 'styles', items: [ 'Styles', 'Format', 'Font', 'FontSize' ] },
                    { name: 'colors', items: [ 'TextColor', 'BGColor' ] },
                    { name: 'tools', items: [ 'Maximize' ] }
                ],
                removePlugins: 'elementspath',
                resize_enabled: true
            });
        }
    });
});

// Обработка отправки формы - синхронизация данных CKEditor
document.addEventListener('submit', function(e) {
    for (let instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
});
