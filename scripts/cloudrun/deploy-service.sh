#!/usr/bin/env bash
set -euo pipefail

: "${PROJECT_ID:?Set PROJECT_ID}"
: "${REGION:?Set REGION}"
: "${SERVICE_NAME:?Set SERVICE_NAME}"
: "${IMAGE_URI:?Set IMAGE_URI}"
: "${SERVICE_ACCOUNT:?Set SERVICE_ACCOUNT}"

PORT="${PORT:-8080}"
MEMORY="${MEMORY:-512Mi}"
CPU="${CPU:-1}"
CONCURRENCY="${CONCURRENCY:-80}"
REQUEST_TIMEOUT="${REQUEST_TIMEOUT:-300}"
MIN_INSTANCES="${MIN_INSTANCES:-0}"
MAX_INSTANCES="${MAX_INSTANCES:-10}"
INGRESS="${INGRESS:-internal-and-cloud-load-balancing}"
NO_TRAFFIC="${NO_TRAFFIC:-false}"

deploy_args=(
  run
  deploy
  "${SERVICE_NAME}"
  --project "${PROJECT_ID}"
  --region "${REGION}"
  --platform managed
  --image "${IMAGE_URI}"
  --service-account "${SERVICE_ACCOUNT}"
  --port "${PORT}"
  --memory "${MEMORY}"
  --cpu "${CPU}"
  --concurrency "${CONCURRENCY}"
  --timeout "${REQUEST_TIMEOUT}"
  --min-instances "${MIN_INSTANCES}"
  --max-instances "${MAX_INSTANCES}"
  --ingress "${INGRESS}"
  --allow-unauthenticated
  --startup-probe "httpGet.path=/ready/,httpGet.port=${PORT},timeoutSeconds=5,periodSeconds=10,failureThreshold=12"
)

if [[ -n "${ENV_VARS_FILE:-}" ]]; then
  deploy_args+=(--env-vars-file "${ENV_VARS_FILE}")
fi

if [[ -n "${SECRETS_SPEC:-}" ]]; then
  deploy_args+=(--set-secrets "${SECRETS_SPEC}")
fi

if [[ -n "${CLOUD_SQL_CONNECTION_NAME:-}" ]]; then
  deploy_args+=(--set-cloudsql-instances "${CLOUD_SQL_CONNECTION_NAME}")
fi

if [[ "${NO_TRAFFIC}" == "true" ]]; then
  deploy_args+=(--no-traffic)
fi

gcloud "${deploy_args[@]}"
