// Инициализация TinyMCE для текстовых полей
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация для полей новостей и других текстовых полей
    const textareaIds = [
        'id_paragraph_1',
        'id_paragraph_1_uz',
        'id_paragraph_1_ru',
        'id_paragraph_1_en',
        'id_paragraph_2',
        'id_paragraph_2_uz',
        'id_paragraph_2_ru',
        'id_paragraph_2_en',
        'id_text_content',
        'id_text_content_uz',
        'id_text_content_ru',
        'id_text_content_en'
    ];
    
    // Проверяем, что TinyMCE загружен
    if (typeof tinymce === 'undefined') {
        console.error('TinyMCE не загружен');
        return;
    }
    
    // Инициализация TinyMCE для всех полей
    tinymce.init({
        selector: textareaIds.map(id => '#' + id).join(', '),
        height: 400,
        menubar: false,
        plugins: [
            'advlist', 'autolink', 'lists', 'link', 'charmap', 'preview',
            'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
            'insertdatetime', 'media', 'table', 'code', 'help', 'wordcount'
        ],
        toolbar: 'undo redo | formatselect | ' +
            'bold italic underline strikethrough | ' +
            'alignleft aligncenter alignright alignjustify | ' +
            'bullist numlist outdent indent | ' +
            'removeformat | link | code',
        content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }',
        // Отключаем вставку изображений
        paste_data_images: false,
        images_upload_url: false,
        automatic_uploads: false,
        file_picker_types: '',
        // Настройки для безопасности
        valid_elements: 'p,br,strong/b,em/i,u,strike,s,ul,ol,li,blockquote,a[href|target|rel],h1,h2,h3,h4,h5,h6',
        valid_children: '+body[style]',
        extended_valid_elements: 'a[href|target|rel|title]',
        // Автоматическая синхронизация при отправке формы
        setup: function(editor) {
            editor.on('init', function() {
                // Редактор инициализирован
            });
        }
    });
});
