# Настройка интеграции с Instagram

Эта инструкция поможет вам настроить получение постов из Instagram для отображения на сайте.

## Требования

1. **Instagram Business** или **Creator** аккаунт (личный аккаунт не подойдет)
2. **Facebook Business** аккаунт
3. **Facebook App** с подключенным Instagram

## Шаги настройки

### 1. Преобразование аккаунта Instagram в Business

1. Откройте приложение Instagram на мобильном устройстве
2. Перейдите в настройки профиля
3. Выберите "Переключиться на профессиональный аккаунт"
4. Выберите "Business" или "Creator"
5. Подключите аккаунт к Facebook Page (создайте страницу, если её нет)

### 2. Создание Facebook App

1. Перейдите на [Facebook Developers](https://developers.facebook.com/)
2. Создайте новое приложение:
   - Нажмите "Создать приложение"
   - Выберите тип "Другое" или "Бизнес"
   - Заполните название и контактный email
3. Добавьте продукт "Instagram":
   - В настройках приложения найдите раздел "Products"
   - Добавьте "Instagram Graph API"
4. Настройте Instagram Basic Display:
   - Перейдите в "Instagram" → "Basic Display"
   - Добавьте "Valid OAuth Redirect URIs" (можно использовать `http://localhost:8000` для тестирования)

### 3. Получение Access Token

#### Вариант 1: Долгосрочный токен (рекомендуется)

1. Перейдите в [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Выберите ваше приложение в выпадающем списке
3. Получите краткосрочный токен:
   - Нажмите "Generate Access Token"
   - Выберите права: `instagram_basic`, `pages_read_engagement`, `instagram_content_publish` (если нужно)
   - Скопируйте токен
4. Обменяйте краткосрочный токен на долгосрочный:
   ```
   https://graph.facebook.com/v18.0/oauth/access_token?
     grant_type=fb_exchange_token&
     client_id={YOUR_APP_ID}&
     client_secret={YOUR_APP_SECRET}&
     fb_exchange_token={SHORT_LIVED_TOKEN}
   ```
   Замените:
   - `{YOUR_APP_ID}` - ID вашего приложения
   - `{YOUR_APP_SECRET}` - Secret вашего приложения (найдите в настройках приложения)
   - `{SHORT_LIVED_TOKEN}` - краткосрочный токен из шага 3

#### Вариант 2: Использование User Access Token

1. В Graph API Explorer получите User Access Token с правами `instagram_basic`
2. Используйте этот токен напрямую (он будет действителен ~60 дней)

### 4. Получение Instagram Business Account ID

1. Используя ваш Access Token, выполните запрос:
   ```
   GET https://graph.instagram.com/me?fields=id,username&access_token={YOUR_ACCESS_TOKEN}
   ```
2. В ответе вы получите `id` - это и есть ваш Instagram Business Account ID

### 5. Настройка в Django

Добавьте следующие переменные в ваш `.env` файл или в настройки Django:

```env
INSTAGRAM_USERNAME=yecgilam
INSTAGRAM_ACCESS_TOKEN=your_long_lived_access_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_instagram_business_account_id_here
```

Или добавьте в `config/settings/local.py`:

```python
INSTAGRAM_USERNAME = "yecgilam"
INSTAGRAM_ACCESS_TOKEN = "your_token_here"
INSTAGRAM_BUSINESS_ACCOUNT_ID = "your_account_id_here"
```

### 6. Применение миграций

```bash
docker compose -f docker-compose.local.yml run --rm django python manage.py migrate
```

### 7. Синхронизация постов

Запустите команду для получения постов из Instagram:

```bash
docker compose -f docker-compose.local.yml run --rm django python manage.py sync_instagram_posts
```

Вы можете указать количество постов для получения:

```bash
docker compose -f docker-compose.local.yml run --rm django python manage.py sync_instagram_posts --limit 20
```

### 8. Автоматическая синхронизация (опционально)

Для автоматической синхронизации добавьте задачу в cron или используйте Celery:

```python
# В tasks.py (если используете Celery)
from celery import shared_task
from django.core.management import call_command

@shared_task
def sync_instagram():
    call_command('sync_instagram_posts', limit=12)
```

Или добавьте в crontab:

```bash
# Синхронизация каждый час
0 * * * * cd /path/to/project && docker compose -f docker-compose.local.yml run --rm django python manage.py sync_instagram_posts
```

## Использование API

После синхронизации посты будут доступны через API:

```
GET /api/instagram-posts/
```

Ответ будет содержать список опубликованных постов с пагинацией:

```json
{
  "count": 12,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "instagram_id": "123456789",
      "post_type": "IMAGE",
      "caption": "Описание поста...",
      "permalink": "https://www.instagram.com/p/...",
      "thumbnail_url": "https://...",
      "media_url": "https://...",
      "like_count": 100,
      "comments_count": 5,
      "timestamp": "2024-01-15T10:30:00Z",
      "is_published": true
    }
  ]
}
```

## Управление постами в админке

Посты можно просматривать и управлять их видимостью в Django Admin:

- `/admin/catalog/instagrampost/` - список всех постов
- Можно скрыть пост, сняв галочку "Публикация" (`is_published`)

## Типы постов

Система поддерживает три типа постов:
- **IMAGE** - одиночное изображение
- **VIDEO** - видео
- **CAROUSEL_ALBUM** - карусель (несколько изображений)

## Ограничения Instagram API

- Access Token имеет срок действия (долгосрочные токены действуют ~60 дней)
- Для продления токена используйте [Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
- Instagram Graph API имеет лимиты на количество запросов
- Для получения всех постов может потребоваться пагинация (реализована в команде)

## Альтернативные методы (не рекомендуется)

Если официальный API не подходит, можно использовать:
- Библиотеку `instagrapi` (неофициальная, может нарушать ToS Instagram)
- Парсинг страницы (нарушает ToS Instagram)

**Внимание**: Использование неофициальных методов может привести к блокировке аккаунта Instagram.

## Устранение неполадок

### Ошибка: "Invalid OAuth access token"
- Проверьте, что токен не истек
- Убедитесь, что токен имеет необходимые права
- Обновите токен через Token Debugger

### Ошибка: "User does not have permission"
- Убедитесь, что аккаунт Instagram подключен к Facebook Page
- Проверьте, что используете Business или Creator аккаунт

### Ошибка: "Invalid user id"
- Проверьте правильность `INSTAGRAM_BUSINESS_ACCOUNT_ID`
- Убедитесь, что используете ID аккаунта, а не username

## Полезные ссылки

- [Instagram Graph API Documentation](https://developers.facebook.com/docs/instagram-api)
- [Getting Started with Instagram Graph API](https://developers.facebook.com/docs/instagram-api/getting-started)
- [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
