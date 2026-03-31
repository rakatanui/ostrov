Django application for publishing the legends of Ostrov.

The project provides:

- public website with multilingual content
- Django admin for editorial work and moderation
- PostgreSQL database
- local development with Docker Compose
- production deployment to Google Cloud:
  - Cloud Run
  - Cloud SQL for PostgreSQL
  - Secret Manager
  - Google Cloud Storage
  - Artifact Registry
  - Cloud Build trigger for automatic deployment from `main`

## Stack

- Python 3.12
- Django 6
- PostgreSQL
- Docker Compose for local development
- Gunicorn in production
- Google Cloud Run for app hosting
- Google Cloud Storage for `static` and `media`
- Cloud Build for CI/CD

## Project structure

```text
.
├── cloudbuild.image.yaml
├── cloudbuild.production.yaml
├── cloudrun.production.env.yaml
├── compose.yaml
├── docker/
│   └── web/
│       ├── Dockerfile
│       ├── entrypoint.sh
│       └── start-web.sh
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
├── scripts/
│   └── cloudrun/
│       ├── build-image.sh
│       ├── deploy-service.sh
│       ├── render-env-file.sh
│       └── run-job.sh
├── src/
│   ├── manage.py
│   ├── config/
│   └── apps/
└── Makefile
````

## Local development

### Requirements

* Docker
* Docker Compose

### Start locally

```bash
cp .env.example .env
docker compose up --build
```

Application:

* site: [http://localhost:8000/](http://localhost:8000/)
* admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)
* health: [http://localhost:8000/health/](http://localhost:8000/health/)
* ready: [http://localhost:8000/ready/](http://localhost:8000/ready/)

### Common local commands

Apply migrations:

```bash
docker compose exec web python manage.py migrate
```

Create superuser:

```bash
docker compose exec web python manage.py createsuperuser
```

Collect static locally if needed:

```bash
docker compose exec web python manage.py collectstatic --noinput
```

## Production architecture

Production is built around Google Cloud.

Components:

* **Cloud Run**: Django application
* **Cloud SQL for PostgreSQL**: database
* **Secret Manager**: secrets
* **Google Cloud Storage**:

  * one bucket for `static`
  * one bucket for `media`
* **Artifact Registry**: container images
* **Cloud Build**: automatic deployment pipeline

### Important notes

* secrets are **not stored in the repository**
* production service reads secrets from **Secret Manager**
* `static` and `media` are stored in **GCS**
* the production env template is **YAML**, not dotenv
* the final custom-domain setup is intended to run behind a **Google Cloud external Application Load Balancer**
* direct `run.app` access is acceptable for bootstrap/debug, but not the final public entrypoint for `ostrov.quest`

## Production configuration files

### `cloudrun.production.env.yaml`

This file is the **non-secret production environment template**.

It contains placeholders such as:

* `__GOOGLE_CLOUD_PROJECT__`
* `__CLOUD_SQL_CONNECTION_NAME__`
* `__GCS_STATIC_BUCKET_NAME__`
* `__GCS_MEDIA_BUCKET_NAME__`

It must be rendered before manual deployment.

### `cloudrun.production.rendered.env.yaml`

This is the rendered file used by manual deployment scripts.

It is generated from `cloudrun.production.env.yaml` and should not be edited manually.

### Secrets

The following values must come from Secret Manager:

* `DJANGO_SECRET_KEY`
* `POSTGRES_PASSWORD`
* `DJANGO_SUPERUSER_PASSWORD`

## Manual production deployment

Manual deployment exists for:

* first bootstrap
* debugging
* emergency/manual rollback
* validating infrastructure before enabling automatic deployment

It is **not** the preferred long-term release path.

### 1. Set required variables

Example:

```bash
export PROJECT_ID="your-project-id"
export REGION="europe-west1"
export REPOSITORY="ostrov-quest"
export IMAGE_NAME="ostrov-quest-web"
export IMAGE_TAG="$(date +%Y%m%d-%H%M%S)"
export IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE_NAME}:${IMAGE_TAG}"

export SERVICE_NAME="ostrov-quest-web"
export SERVICE_ACCOUNT="ostrov-quest-run@${PROJECT_ID}.iam.gserviceaccount.com"
export CLOUD_SQL_CONNECTION_NAME="${PROJECT_ID}:${REGION}:ostrov-quest-db"

export STATIC_BUCKET="ostrov-quest-static"
export MEDIA_BUCKET="ostrov-quest-media"

export ENV_TEMPLATE_FILE="cloudrun.production.env.yaml"
export ENV_RENDERED_FILE="cloudrun.production.rendered.env.yaml"
export SECRETS_SPEC="DJANGO_SECRET_KEY=django-secret-key:latest,POSTGRES_PASSWORD=postgres-password:latest,DJANGO_SUPERUSER_PASSWORD=django-superuser-password:latest"
export INGRESS="all"
```

### 2. Render production env YAML

```bash
make cloud-render-env
```

This renders `cloudrun.production.rendered.env.yaml` using current shell variables.

### 3. Build image

```bash
make cloud-build
```

This uses `scripts/cloudrun/build-image.sh`, which builds through `cloudbuild.image.yaml`.

### 4. Deploy Cloud Run service

```bash
make cloud-deploy
```

### 5. Run release tasks

Check deploy settings:

```bash
make cloud-check
```

Apply migrations:

```bash
make cloud-migrate
```

Collect static:

```bash
make cloud-collectstatic
```

Ensure admin user exists:

```bash
make cloud-superuser
```

### 6. Inspect service

Get service URL:

```bash
gcloud run services describe "$SERVICE_NAME" \
  --region="$REGION" \
  --format='value(status.url)'
```

Check health endpoints:

```bash
curl -i "SERVICE_URL/health/"
curl -i "SERVICE_URL/ready/"
```

## Automatic production deployment

Automatic deployment is the preferred production path.

### Trigger source

* GitHub repository
* branch: `main`

### Deployment flow

On push/merge to `main`, Cloud Build runs `cloudbuild.production.yaml`.

Pipeline sequence:

1. validate required substitutions
2. render production env file
3. build image
4. push image to Artifact Registry
5. deploy Cloud Run revision with **no traffic**
6. deploy/update release jobs
7. run release jobs in sequence:

   * `check --deploy`
   * `migrate`
   * `collectstatic`
   * `ensure_superuser`
8. route traffic to latest revision **only if all previous steps succeed**

This is the primary release mechanism.

## Cloud Build trigger setup

### Connect GitHub repository

In Google Cloud Console:

1. open **Cloud Build**
2. open **Triggers**
3. click **Create trigger**
4. connect the GitHub repository
5. choose:

   * event: **Push to a branch**
   * branch: `^main$`
   * configuration: **Cloud Build configuration file**
   * file location: `cloudbuild.production.yaml`

### Required substitutions for trigger

Set these substitutions in the trigger:

* `_REGION`
* `_REPOSITORY`
* `_SERVICE_NAME`
* `_IMAGE_NAME`
* `_SERVICE_ACCOUNT`
* `_CLOUD_SQL_CONNECTION_NAME`
* `_GOOGLE_CLOUD_PROJECT`
* `_GCS_STATIC_BUCKET_NAME`
* `_GCS_MEDIA_BUCKET_NAME`
* `_SECRETS_SPEC`
* `_INGRESS`

Typical example values:

```text
_REGION=europe-west1
_REPOSITORY=ostrov-quest
_SERVICE_NAME=ostrov-quest-web
_IMAGE_NAME=ostrov-quest-web
_SERVICE_ACCOUNT=ostrov-quest-run@your-project-id.iam.gserviceaccount.com
_CLOUD_SQL_CONNECTION_NAME=your-project-id:europe-west1:ostrov-quest-db
_GOOGLE_CLOUD_PROJECT=your-project-id
_GCS_STATIC_BUCKET_NAME=ostrov-quest-static
_GCS_MEDIA_BUCKET_NAME=ostrov-quest-media
_SECRETS_SPEC=DJANGO_SECRET_KEY=django-secret-key:latest,POSTGRES_PASSWORD=postgres-password:latest,DJANGO_SUPERUSER_PASSWORD=django-superuser-password:latest
_INGRESS=internal-and-cloud-load-balancing
```

### Required IAM for Cloud Build service account

The Cloud Build service account must be able to:

* push images to Artifact Registry
* deploy/update Cloud Run services
* deploy/update/execute Cloud Run jobs
* impersonate/use the runtime service account if required
* access Secret Manager references used by deployment
* work with Cloud SQL attachment settings used by Cloud Run

At minimum, review and grant the necessary roles for your environment before enabling the trigger.

## Service account for runtime

The Cloud Run runtime service account should have at least:

* access to Cloud SQL
* access to Secret Manager
* access to write objects into configured GCS buckets

## Google Cloud Storage

The current production setup assumes:

* one bucket for `static`
* one bucket for `media`

For the baseline setup used here:

* application writes objects to GCS
* application generates public object URLs
* `static` and `media` buckets must be readable according to the chosen production policy
* if you use direct public GCS URLs, do **not** enable a configuration that blocks public reads for those buckets

## Admin access

The Django admin is part of the same public application service.

That means:

* `/admin/` is network-reachable through the application endpoint
* access control is provided by Django authentication
* passwords and admin-user management matter
* this is acceptable for the current setup, but should be treated as an intentional decision

## Common production commands

Render env file:

```bash
make cloud-render-env
```

Build image:

```bash
make cloud-build
```

Deploy service:

```bash
make cloud-deploy
```

Run production checks:

```bash
make cloud-check
```

Run migrations:

```bash
make cloud-migrate
```

Collect static:

```bash
make cloud-collectstatic
```

Ensure superuser:

```bash
make cloud-superuser
```

Show logs manually:

```bash
gcloud logging read \
'resource.type="cloud_run_revision" AND resource.labels.service_name="ostrov-quest-web"' \
--project="$PROJECT_ID" \
--limit=50 \
--order=desc
```

## Rollback

If a new revision is bad, rollback by routing traffic back to the previous healthy revision:

```bash
gcloud run services update-traffic "$SERVICE_NAME" \
  --region="$REGION" \
  --to-revisions REVISION_NAME=100
```

Use `gcloud run revisions list` to find the previous revision.

## Troubleshooting

### Startup probe fails with `DisallowedHost`

Add probe host values such as `127.0.0.1` and `localhost` to `DJANGO_ALLOWED_HOSTS` for Cloud Run startup checks.

### Service starts but `/ready/` returns database unavailable

Check:

* Cloud SQL instance exists and is running
* Cloud Run service is attached to the correct Cloud SQL instance
* `POSTGRES_DB` and `POSTGRES_USER` are correct
* secret `postgres-password` matches the actual database user password

### Static loads locally but not in production

Check:

* correct GCS bucket names
* storage configuration in production settings
* bucket read policy
* successful `collectstatic` job execution

### Admin login fails

Re-run:

```bash
make cloud-superuser
```

or update `django-superuser-password` in Secret Manager and run the command again.

## Recommended workflow

### Day-to-day production workflow

1. make changes
2. open PR
3. review
4. merge to `main`
5. Cloud Build trigger deploys automatically

### Manual workflow

Use manual deployment only when:

* bootstrapping infrastructure
* debugging deployment
* recovering from CI/CD issues
* validating environment changes

## Current status

The repository supports:

* local development with Docker Compose
* manual Cloud Run deployment
* automatic Cloud Build deployment from `main`

The intended long-term production path is:

**GitHub `main` -> Cloud Build trigger -> Artifact Registry -> Cloud Run -> release jobs -> traffic switch**
