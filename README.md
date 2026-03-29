# Легенды Острова

Существующий Django-монолит для сайта `ostrov.quest`, подготовленный к локальной разработке и production deployment в Google Cloud по схеме:

- Cloud Run для веб-приложения
- Cloud SQL for PostgreSQL для базы данных
- Secret Manager для секретов
- Cloud Storage для `static` и `media`
- Artifact Registry для контейнерного образа
- `gcloud builds submit` / Cloud Build для сборки образа
- Cloud Run Jobs для release-задач
- custom domain `ostrov.quest` через global external Application Load Balancer

## Local Development

Локальная разработка остаётся через Docker Compose.

1. Создай локальный env-файл:

```powershell
Copy-Item .env.example .env
```

2. Подними проект:

```powershell
docker compose up --build
```

3. Открой:

- сайт: `http://localhost:8000/`
- healthcheck: `http://localhost:8000/health/`
- readiness: `http://localhost:8000/ready/`
- admin: `http://localhost:8000/admin/`

Контейнер `web` в локальном режиме ждёт PostgreSQL и применяет миграции автоматически. Это локальная-only логика, в production она не используется.

## Production Architecture On Google Cloud

Production-схема:

- Cloud Run service `ostrov-quest-web` с Gunicorn
- Cloud SQL PostgreSQL, подключённый через Unix socket `/cloudsql/INSTANCE_CONNECTION_NAME`
- отдельные buckets для `static` и `media`
- Secret Manager для `DJANGO_SECRET_KEY`, `POSTGRES_PASSWORD`, `DJANGO_SUPERUSER_PASSWORD` и других чувствительных значений
- Artifact Registry для контейнерного образа
- Cloud Run Jobs для `check --deploy`, `migrate`, `collectstatic`, `ensure_superuser`
- global external Application Load Balancer + serverless NEG перед Cloud Run для production custom domain

В приложении уже настроены:

- `config.settings.production`
- `SECURE_PROXY_SSL_HEADER`
- secure cookies
- redirect exemption для `/health/` и `/ready/`
- readiness endpoint `/ready/`
- health endpoint `/health/`
- Gunicorn startup через `0.0.0.0:$PORT`
- GCS-backed storage для `static` и `media`
- Cloud SQL-ready database configuration

## Production Static And Media Strategy

Для текущего сайта используется один простой production-вариант:

- `static` хранятся в отдельном GCS bucket и публично читаются браузером
- `media` хранятся в отдельном GCS bucket и тоже публично читаются браузером
- приложение пишет в buckets через `django-storages`
- браузер забирает файлы по публичным URL

Это осознанный выбор для текущего проекта:

- сайт публичный
- `static` обязаны быть публично читаемыми, иначе сломается admin и публичные страницы
- текущие `media` не являются приватными пользовательскими файлами; это контент сайта, который должен открываться в браузере без signed URL-логики

Следствия этой стратегии:

- buckets `static` и `media` должны быть публично читаемыми
- используется Uniform Bucket-Level Access
- доступ на чтение для браузера выдаётся через bucket IAM `allUsers -> roles/storage.objectViewer`
- signed URL для baseline production-варианта не используются

Если позже появятся приватные пользовательские файлы, для `media` потребуется отдельная стратегия доставки. Текущая production-подготовка этого не делает.

## Required Google Cloud Services

Нужно включить и подготовить:

- Cloud Run
- Cloud Build
- Artifact Registry
- Cloud SQL Admin API
- Secret Manager API
- Cloud Storage
- Certificate Manager / Managed SSL certificate для load balancer
- External Application Load Balancer с serverless NEG

Service account Cloud Run должен иметь минимум:

- `roles/cloudsql.client`
- `roles/secretmanager.secretAccessor`
- `roles/storage.objectAdmin` на buckets для `static` и `media`

## Required Environment Variables

Шаблоны:

- локальная разработка: `.env.example`
- production: `.env.production.example`

Ключевые production env vars:

- `DJANGO_SETTINGS_MODULE=config.settings.production`
- `DJANGO_ALLOWED_HOSTS=ostrov.quest,www.ostrov.quest`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://ostrov.quest,https://www.ostrov.quest`
- `DJANGO_TIME_ZONE=UTC`
- `DJANGO_LOG_LEVEL=INFO`
- `CLOUD_SQL_CONNECTION_NAME=project:region:instance`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD` через Secret Manager
- `GCS_STATIC_BUCKET_NAME`
- `GCS_MEDIA_BUCKET_NAME`
- `GCS_STATIC_PREFIX=static`
- `GCS_MEDIA_PREFIX=media`
- `GUNICORN_WORKERS`
- `GUNICORN_THREADS`
- `GUNICORN_TIMEOUT`

Поддерживаются два способа конфигурации БД:

1. `DATABASE_URL`
2. явные `POSTGRES_*` + `CLOUD_SQL_CONNECTION_NAME`

Для Cloud SQL в Cloud Run рекомендуется второй вариант: он проще и не требует URL-encoding Unix socket path.

## Build Image

Сначала создай Artifact Registry repository, например `ostrov-quest`.

Подготовь переменные:

```bash
export PROJECT_ID="your-project-id"
export REGION="europe-west1"
export REPOSITORY="ostrov-quest"
export IMAGE_NAME="ostrov-quest-web"
export IMAGE_TAG="$(date +%Y%m%d-%H%M%S)"
```

Сборка и push образа в Artifact Registry:

```bash
bash scripts/cloudrun/build-image.sh
```

Скрипт использует:

```bash
gcloud builds submit \
  --project "$PROJECT_ID" \
  --tag "$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$IMAGE_TAG" \
  --file docker/web/Dockerfile \
  .
```

## Push Image

Отдельный push не нужен: `gcloud builds submit --tag ...` сразу собирает и публикует образ в Artifact Registry.

Если нужен явный URI образа:

```bash
export IMAGE_URI="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$IMAGE_TAG"
```

## Attach Secrets

Создай секреты в Secret Manager:

```bash
printf '%s' 'replace-with-real-django-secret-key' | gcloud secrets create django-secret-key --data-file=-
printf '%s' 'replace-with-real-db-password' | gcloud secrets create postgres-password --data-file=-
printf '%s' 'replace-with-real-superuser-password' | gcloud secrets create django-superuser-password --data-file=-
```

Если секрет уже существует, используй новую версию:

```bash
printf '%s' 'new-value' | gcloud secrets versions add django-secret-key --data-file=-
```

Строка для деплоя:

```bash
export SECRETS_SPEC="DJANGO_SECRET_KEY=django-secret-key:latest,POSTGRES_PASSWORD=postgres-password:latest,DJANGO_SUPERUSER_PASSWORD=django-superuser-password:latest"
```

Не клади реальные секреты в `.env.production`.

## Attach Cloud SQL

Подготовь Cloud SQL instance и базу данных. Затем:

```bash
export CLOUD_SQL_CONNECTION_NAME="your-project-id:europe-west1:ostrov-quest-db"
export SERVICE_ACCOUNT="ostrov-quest-run@${PROJECT_ID}.iam.gserviceaccount.com"
```

Cloud Run service и Cloud Run Jobs получают подключение к Cloud SQL через:

- `--set-cloudsql-instances "$CLOUD_SQL_CONNECTION_NAME"`
- env `CLOUD_SQL_CONNECTION_NAME`

В production settings это приводит Django к Unix socket host:

```text
/cloudsql/your-project-id:europe-west1:ostrov-quest-db
```

## Configure Buckets

Создай два buckets:

```bash
gcloud storage buckets create "gs://ostrov-quest-static" --project "$PROJECT_ID" --location "$REGION" --uniform-bucket-level-access
gcloud storage buckets create "gs://ostrov-quest-media" --project "$PROJECT_ID" --location "$REGION" --uniform-bucket-level-access
```

Выдай service account доступ на запись:

```bash
gcloud storage buckets add-iam-policy-binding "gs://ostrov-quest-static" \
  --member "serviceAccount:$SERVICE_ACCOUNT" \
  --role "roles/storage.objectAdmin"

gcloud storage buckets add-iam-policy-binding "gs://ostrov-quest-media" \
  --member "serviceAccount:$SERVICE_ACCOUNT" \
  --role "roles/storage.objectAdmin"
```

Выдай публичный доступ на чтение для браузеров:

```bash
gcloud storage buckets add-iam-policy-binding "gs://ostrov-quest-static" \
  --member "allUsers" \
  --role "roles/storage.objectViewer"

gcloud storage buckets add-iam-policy-binding "gs://ostrov-quest-media" \
  --member "allUsers" \
  --role "roles/storage.objectViewer"
```

Non-secret значения для production env-файла:

```dotenv
GOOGLE_CLOUD_PROJECT=your-project-id
GCS_STATIC_BUCKET_NAME=ostrov-quest-static
GCS_MEDIA_BUCKET_NAME=ostrov-quest-media
GCS_STATIC_PREFIX=static
GCS_MEDIA_PREFIX=media
```

Важно:

- текущая baseline-стратегия требует публичного чтения обоих buckets
- если в организации принудительно включён Public Access Prevention, браузер не сможет читать `static`/`media` по прямым GCS URL
- если позже захочется CDN или отдельный asset hostname, можно переопределить `DJANGO_STATIC_URL` и `DJANGO_MEDIA_URL`, не меняя storage backend

## Deploy To Cloud Run

Подготовь production env-файл без секретов, например `.env.production`, на основе `.env.production.example`.

Минимальный набор экспортов:

```bash
export PROJECT_ID="your-project-id"
export REGION="europe-west1"
export SERVICE_NAME="ostrov-quest-web"
export IMAGE_URI="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE_NAME:$IMAGE_TAG"
export SERVICE_ACCOUNT="ostrov-quest-run@${PROJECT_ID}.iam.gserviceaccount.com"
export ENV_VARS_FILE=".env.production"
export SECRETS_SPEC="DJANGO_SECRET_KEY=django-secret-key:latest,POSTGRES_PASSWORD=postgres-password:latest,DJANGO_SUPERUSER_PASSWORD=django-superuser-password:latest"
export CLOUD_SQL_CONNECTION_NAME="your-project-id:europe-west1:ostrov-quest-db"
```

По умолчанию deploy script использует:

- `--allow-unauthenticated`, потому что сайт публичный
- `--ingress internal-and-cloud-load-balancing`, потому что финальный production-вариант предполагает доступ через global external Application Load Balancer

Если нужно временно проверить сервис напрямую через `run.app` до подключения load balancer, можно сделать разовый deploy с:

```bash
export INGRESS="all"
```

Деплой сервиса:

```bash
bash scripts/cloudrun/deploy-service.sh
```

Скрипт выполняет `gcloud run deploy` и настраивает:

- образ из Artifact Registry
- service account
- `PORT=8080`
- startup probe на `/ready/`
- env vars из файла
- secrets из Secret Manager
- Cloud SQL connection

## Run Migrations

Release-задачи выполняются отдельно от веб-сервиса через Cloud Run Jobs.

Прогон миграций:

```bash
bash scripts/cloudrun/run-job.sh ostrov-quest-migrate python manage.py migrate --noinput
```

или:

```bash
make cloud-migrate
```

## Run Collectstatic

`collectstatic` пишет прямо в GCS-backed static storage:

```bash
bash scripts/cloudrun/run-job.sh ostrov-quest-collectstatic python manage.py collectstatic --noinput
```

или:

```bash
make cloud-collectstatic
```

## Create Superuser

Для bootstrap admin используй отдельный job:

```bash
bash scripts/cloudrun/run-job.sh ostrov-quest-superuser python manage.py ensure_superuser --skip-if-missing
```

или:

```bash
make cloud-superuser
```

Команда `ensure_superuser` создаёт или обновляет superuser из:

- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_EMAIL`
- `DJANGO_SUPERUSER_PASSWORD`

Если env не заданы и передан `--skip-if-missing`, job завершается без ошибки.

## Check Deploy Configuration

Перед миграциями полезно прогнать:

```bash
bash scripts/cloudrun/run-job.sh ostrov-quest-check python manage.py check --deploy
```

или:

```bash
make cloud-check
```

## Verify Deployment

Есть два рабочих сценария проверки.

Если сервис ещё не стоит за load balancer и ты временно деплоил с `INGRESS=all`:

```bash
curl -i "https://YOUR_RUN_APP_URL/health/"
curl -i "https://YOUR_RUN_APP_URL/ready/"
```

Если финальная схема уже собрана через external Application Load Balancer:

```bash
curl -i "https://ostrov.quest/health/"
curl -i "https://ostrov.quest/ready/"
```

Ожидаемо:

- `/health/` возвращает `200 {"status":"ok"}`
- `/ready/` возвращает `200 {"status":"ok","database":"ok"}`

Также проверь:

- `/admin/` загружается со стилями
- загрузка изображения в admin пишет файл в GCS media bucket
- публичные страницы отдают ссылки на файлы из публичных `static`/`media` buckets
- прямой запрос к одному из объектов `media` или `static` возвращает `200`, а не `403`

## Public Cloud Run Service And Django Admin

Сервис остаётся `allow-unauthenticated`, потому что это публичный сайт.

Это означает:

- публичные страницы сайта доступны без IAM-аутентификации
- `/admin/` тоже доступен по сети
- защита `/admin/` строится на обычной Django authentication, CSRF и secure session cookies

Для текущего проекта это приемлемо, потому что:

- admin не является анонимно доступным по содержимому, только по сетевому адресу
- `DEBUG=False`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`
- `SECURE_SSL_REDIRECT=True`
- `X_FRAME_OPTIONS="DENY"`
- стандартные password validators Django включены

Дополнительное минимальное усиление на инфраструктурном уровне уже учтено в deploy script: финальный ingress по умолчанию ограничен режимом `internal-and-cloud-load-balancing`, чтобы production-трафик шёл через load balancer, а не напрямую в публичный `run.app` endpoint.

## Recommended Release Workflow

Практический порядок:

1. Собрать и запушить образ в Artifact Registry.
2. Создать buckets, назначить service account доступ на запись и публичный доступ на чтение.
3. Задеплоить Cloud Run service с env vars, secrets и Cloud SQL attachment.
4. Прогнать `check --deploy`.
5. Прогнать `migrate`.
6. Прогнать `collectstatic`.
7. При необходимости выполнить `ensure_superuser`.
8. Проверить `/health/`, `/ready/`, `/admin/`, доступность `static` и `media`.
9. Подключить сервис к global external Application Load Balancer и домену `ostrov.quest`.
10. Для финального production оставить ingress `internal-and-cloud-load-balancing`.

Миграции и `collectstatic` не запускаются автоматически на старте web-контейнера.

## Notes About Custom Domain And Load Balancer

Этот проект подготовлен для работы за custom domain `ostrov.quest` через global external Application Load Balancer.

Что уже учтено в приложении:

- `SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")`
- `SESSION_COOKIE_SECURE = True`
- `CSRF_COOKIE_SECURE = True`
- `DEBUG = False` в production
- `ALLOWED_HOSTS` и `CSRF_TRUSTED_ORIGINS` читаются из env
- `/health/` и `/ready/` исключены из `SECURE_SSL_REDIRECT`, поэтому HTTP probes не ломают startup/readiness flow

Рекомендуемый production-вариант:

- external Application Load Balancer
- HTTPS frontend
- managed certificate
- serverless NEG на Cloud Run service
- redirect `www -> apex` и `http -> https` на уровне load balancer, а не в Django-коде

Это проще и надёжнее, чем реализовывать canonical redirect внутри приложения.

## Typical Troubleshooting Steps

`/ready/` возвращает `503`:

- проверь `CLOUD_SQL_CONNECTION_NAME`
- проверь, что Cloud Run service и jobs задеплоены с `--set-cloudsql-instances`
- проверь `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- проверь роль `roles/cloudsql.client`

Admin без CSS:

- не выполнен `collectstatic`
- неверно настроен `GCS_STATIC_BUCKET_NAME`
- service account не имеет доступа к static bucket
- static bucket не имеет публичного чтения для браузеров

Загрузка media не работает:

- отсутствует доступ service account к media bucket
- media bucket не имеет публичного чтения для браузеров
- не настроен `GCS_MEDIA_BUCKET_NAME`
- bucket не существует

`403` или `404` при открытии файлов из `storage.googleapis.com`:

- bucket не получил `allUsers -> roles/storage.objectViewer`
- включён Public Access Prevention и публичное чтение заблокировано организационной политикой
- `DJANGO_STATIC_URL` или `DJANGO_MEDIA_URL` указывают не туда

`403 CSRF verification failed`:

- проверь `DJANGO_CSRF_TRUSTED_ORIGINS`
- для `ostrov.quest` должны быть абсолютные HTTPS origins, например `https://ostrov.quest`

Бесконечный SSL redirect:

- проверь, что перед приложением используется HTTPS
- проверь `X-Forwarded-Proto`
- `/health/` и `/ready/` уже исключены из redirect logic; если редиректится остальной сайт, проблема обычно в proxy headers или неверной схеме на внешнем прокси

Cloud Run стартует, но приложение недоступно:

- контейнер должен слушать `0.0.0.0:$PORT`
- production image использует Gunicorn и читает `PORT` из env
- startup probe настроен на `/ready/`, поэтому приложение не должно принимать трафик до готовности БД
- если deploy выполнен с `INGRESS=internal-and-cloud-load-balancing`, прямой доступ к `run.app` снаружи не является ожидаемым поведением
