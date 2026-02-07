# Настройка интеграции с Instagram

Эта инструкция поможет вам настроить получение постов из Instagram для отображения на сайте.

## Два способа получения постов

### 1. Open Source решение (рекомендуется для начала)

**Преимущества:**
- ✅ Не требует Instagram Business аккаунт
- ✅ Не требует Facebook App
- ✅ Работает с любым публичным профилем
- ✅ Простая настройка
- ✅ Не нарушает ToS (использует публичные данные)

**Ограничения:**
- Работает только с публичными профилями
- Может быть медленнее, чем официальный API
- Рекомендуется использовать задержки между запросами

**Быстрый старт:**
```bash
# Установите зависимости (если еще не установлены)
pip install instaloader

# Синхронизируйте посты
docker compose -f docker-compose.local.yml run --rm django python manage.py sync_instagram_posts_opensource --username yecgilam --limit 12
```

Подробнее см. раздел [Open Source решение](#open-source-решение-через-instaloader)

### 2. Официальный Instagram Business API

**Преимущества:**
- ✅ Официальный API от Instagram/Facebook
- ✅ Более стабильная работа
- ✅ Выше скорость получения данных
- ✅ Работает с приватными профилями (при авторизации)

**Ограничения:**
- Требует Instagram Business или Creator аккаунт
- Требует Facebook Business аккаунт и Facebook App
- Требует настройку Access Token
- Access Token нужно периодически обновлять

Подробнее см. раздел [Официальный Instagram Business API](#официальный-instagram-business-api)

---

## Open Source решение (через Instaloader)

### Требования

1. **Публичный Instagram профиль** (любой, не обязательно Business)
2. **Библиотека instaloader** (уже добавлена в зависимости проекта)

### Установка зависимостей

Если вы используете `pyproject.toml`, установите зависимости:

```bash
pip install -e .
```

Или установите напрямую:

```bash
pip install instaloader==4.10.3
```

### Настройка в Django

Добавьте username в ваш `.env` файл или в настройки Django:

```env
INSTAGRAM_USERNAME=yecgilam
```

Для использования авторизации (рекомендуется для избежания блокировок):

```env
INSTAGRAM_USERNAME=yecgilam
INSTAGRAM_LOGIN_USERNAME=your_instagram_account
INSTAGRAM_LOGIN_PASSWORD=your_password  # Опционально, лучше использовать сессию
```

Или добавьте в `config/settings/local.py`:

```python
INSTAGRAM_USERNAME = "yecgilam"
INSTAGRAM_LOGIN_USERNAME = "your_instagram_account"  # Для авторизации
```

### Настройка сессии в Docker

Для Docker окружения (local и production) сессия Instagram сохраняется в Docker volume и не теряется при перезапуске контейнера или обновлении кода.

**Преимущества:**
- ✅ Сессия сохраняется между перезапусками контейнера
- ✅ Сессия сохраняется при обновлении кода
- ✅ Не нужно создавать сессию заново после каждого деплоя
- ✅ Безопасное хранение в Docker volume

#### 1. Создание сессии (один раз)

**Для production:**
```bash
docker compose -f docker-compose.production.yml run --rm django python manage.py create_instagram_session --username YOUR_INSTAGRAM_USERNAME
```

**Для local разработки:**
```bash
docker compose -f docker-compose.local.yml run --rm django python manage.py create_instagram_session --username YOUR_INSTAGRAM_USERNAME
```

Введите пароль, когда будет запрошен. Сессия будет сохранена в Docker volume:
- Production: `production_instaloader_sessions`
- Local: `apps_local_instaloader_sessions`

#### 2. Использование сессии при синхронизации

После создания сессии, она будет автоматически использоваться при синхронизации:

**Production:**
```bash
docker compose -f docker-compose.production.yml run --rm django python manage.py sync_instagram_posts_opensource --login-username YOUR_INSTAGRAM_USERNAME
```

**Local:**
```bash
docker compose -f docker-compose.local.yml run --rm django python manage.py sync_instagram_posts_opensource --login-username YOUR_INSTAGRAM_USERNAME
```

**Или через настройки в `.env`:**

Добавьте в `.envs/.production/.django` (или `.envs/.local/.django`):
```env
INSTAGRAM_LOGIN_USERNAME=YOUR_INSTAGRAM_USERNAME
```

Тогда команда будет использовать сессию автоматически без указания `--login-username`:

```bash
docker compose -f docker-compose.production.yml run --rm django python manage.py sync_instagram_posts_opensource
```

#### 3. Проверка сохранения сессии

Сессия сохраняется в Docker volume и будет доступна после:
- Перезапуска контейнера
- Обновления кода
- Пересборки образа

Volume монтируется в `/app/.config/instaloader` внутри контейнера.

### Синхронизация постов

Запустите команду для получения постов:

```bash
docker compose -f docker-compose.local.yml run --rm django python manage.py sync_instagram_posts_opensource
```

**Параметры команды:**

- `--username` - Instagram username (по умолчанию из настроек)
- `--limit` - Количество постов для получения (по умолчанию: 12, 0 = все доступные)
- `--all` - Получить все доступные посты
- `--delay` - Задержка между запросами в секундах (по умолчанию: 2.0)

**Примеры:**

```bash
# Получить 20 постов
docker compose -f docker-compose.local.yml run --rm django python manage.py sync_instagram_posts_opensource --limit 20

# Получить все посты с задержкой 3 секунды
docker compose -f docker-compose.local.yml run --rm django python manage.py sync_instagram_posts_opensource --all --delay 3.0

# Получить посты из другого профиля
docker compose -f docker-compose.local.yml run --rm django python manage.py sync_instagram_posts_opensource --username another_profile
```

### Автоматическая синхронизация (опционально)

Для автоматической синхронизации добавьте задачу в cron или используйте Celery:

```python
# В tasks.py (если используете Celery)
from celery import shared_task
from django.core.management import call_command

@shared_task
def sync_instagram_opensource():
    call_command('sync_instagram_posts_opensource', limit=12, delay=2.0)
```

Или добавьте в crontab:

```bash
# Синхронизация каждый час
0 * * * * cd /path/to/project && docker compose -f docker-compose.local.yml run --rm django python manage.py sync_instagram_posts_opensource --limit 12
```

### Работа с отдельного сервера (решение проблемы 429 Too Many Requests)

Если ваш основной сервер заблокирован Instagram (ошибка 429), можно запускать синхронизацию на отдельном сервере (например, в Узбекистане) и передавать данные через JSON или API.

#### Вариант 1: Использование отдельного скрипта с сохранением в JSON

1. **На сервере в Узбекистане** установите зависимости:
```bash
pip install instaloader requests
```

2. **Скопируйте скрипт** `scripts/sync_instagram_standalone.py` на сервер

3. **Создайте сессию Instagram (рекомендуется для избежания блокировок):**
```bash
instaloader -l YOUR_INSTAGRAM_USERNAME
# Введите пароль, сессия будет сохранена
```

4. **Запустите скрипт** для получения постов:

**С авторизацией (рекомендуется):**
```bash
python sync_instagram_standalone.py \
  --username yecgilam \
  --limit 12 \
  --login-username YOUR_INSTAGRAM_USERNAME \
  --delay 5.0 \
  --output instagram_posts.json
```

**Без авторизации (может быть заблокирован):**
```bash
python sync_instagram_standalone.py --username yecgilam --limit 12 --output instagram_posts.json --delay 3.0
```

**С прокси (если IP заблокирован):**
```bash
python sync_instagram_standalone.py \
  --username yecgilam \
  --limit 12 \
  --proxy http://proxy.example.com:8080 \
  --delay 5.0 \
  --output instagram_posts.json
```

4. **Скопируйте JSON файл** на основной сервер

5. **На основном сервере** импортируйте данные:
```bash
docker compose -f docker-compose.local.yml run --rm django python manage.py import_instagram_from_json instagram_posts.json
```

Или с обновлением существующих постов:
```bash
docker compose -f docker-compose.local.yml run --rm django python manage.py import_instagram_from_json instagram_posts.json --update
```

#### Вариант 2: Отправка данных напрямую через API

1. **На сервере в Узбекистане** запустите скрипт с отправкой через API:
```bash
python sync_instagram_standalone.py \
  --username yecgilam \
  --limit 12 \
  --api-url https://your-api-domain.com/api/instagram-posts/ \
  --api-token YOUR_API_TOKEN \
  --delay 3.0
```

**Примечание:** Для работы через API нужно создать endpoint для создания постов (сейчас только чтение). Альтернативно используйте вариант 1 с JSON.

#### Автоматизация через cron

На сервере в Узбекистане можно настроить автоматический запуск:

```bash
# Добавьте в crontab (синхронизация каждый час)
0 * * * * cd /path/to/scripts && python sync_instagram_standalone.py --username yecgilam --limit 12 --output /tmp/instagram_posts.json --delay 3.0 && scp /tmp/instagram_posts.json user@main-server:/tmp/ && ssh user@main-server "cd /path/to/project && docker compose run --rm django python manage.py import_instagram_from_json /tmp/instagram_posts.json"
```

### Устранение неполадок (Open Source)

**Ошибка: "429 Too Many Requests"**
- Instagram заблокировал IP-адрес вашего сервера
- Решение: Используйте отдельный скрипт на другом сервере (см. раздел выше)
- Увеличьте задержку между запросами: `--delay 5.0` или больше

**Ошибка: "Profile not found"**
- Проверьте правильность username
- Убедитесь, что профиль существует и является публичным

**Ошибка: "Connection timeout"**
- Увеличьте задержку между запросами: `--delay 5.0`
- Проверьте интернет-соединение
- Instagram может временно блокировать частые запросы

**Ошибка: "Login required"**
- Профиль является приватным
- Для приватных профилей требуется авторизация (не реализовано в текущей версии)

---

## Официальный Instagram Business API

### Требования

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

## Сравнение методов

| Характеристика | Open Source (Instaloader) | Business API |
|----------------|---------------------------|--------------|
| Требует Business аккаунт | ❌ Нет | ✅ Да |
| Требует Facebook App | ❌ Нет | ✅ Да |
| Работает с публичными профилями | ✅ Да | ✅ Да |
| Работает с приватными профилями | ❌ Нет | ✅ Да (с авторизацией) |
| Настройка | 🟢 Простая | 🟡 Сложная |
| Стабильность | 🟡 Средняя | 🟢 Высокая |
| Скорость | 🟡 Средняя | 🟢 Высокая |
| Соблюдение ToS | ✅ Да (публичные данные) | ✅ Да (официальный API) |
| Обновление токенов | ✅ Не требуется | ❌ Требуется |

**Рекомендация:** Начните с Open Source решения для тестирования. Если нужна более стабильная работа или работа с приватными профилями, переходите на Business API.

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
