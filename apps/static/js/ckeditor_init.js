// Инициализация CKEditor для текстовых полей
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация для основных текстовых полей
    const textareaIds = [
        'id_text_content',
        'id_text_content_ru',
        'id_text_content_en'
    ];
    
    textareaIds.forEach(function(id) {
        const textarea = document.getElementById(id);
        if (textarea) {
            CKEDITOR.replace(id, {
                height: 300,
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
    
    // Обработка inline форм (для динамически добавляемых блоков)
    document.addEventListener('formset:added', function(event) {
        const row = event.target;
        const textareas = row.querySelectorAll('textarea[id*="text_content"]');
        
        textareas.forEach(function(textarea) {
            if (textarea.id && !CKEDITOR.instances[textarea.id]) {
                CKEDITOR.replace(textarea.id, {
                    height: 200,
                    toolbar: [
                        { name: 'basicstyles', items: [ 'Bold', 'Italic', 'Underline' ] },
                        { name: 'paragraph', items: [ 'NumberedList', 'BulletedList', '-', 'Blockquote' ] },
                        { name: 'links', items: [ 'Link', 'Unlink' ] },
                        { name: 'insert', items: [ 'Image' ] }
                    ],
                    removePlugins: 'elementspath',
                    resize_enabled: true
                });
            }
        });
    });
    
    // Очистка при удалении inline формы
    document.addEventListener('formset:removed', function(event) {
        const row = event.target;
        const textareas = row.querySelectorAll('textarea[id*="text_content"]');
        
        textareas.forEach(function(textarea) {
            if (textarea.id && CKEDITOR.instances[textarea.id]) {
                CKEDITOR.instances[textarea.id].destroy();
            }
        });
    });
});

// Обработка отправки формы - синхронизация данных CKEditor
document.addEventListener('submit', function(e) {
    for (let instance in CKEDITOR.instances) {
        CKEDITOR.instances[instance].updateElement();
    }
});
