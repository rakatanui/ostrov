#!/usr/bin/env bash
set -euo pipefail

: "${PROJECT_ID:?Set PROJECT_ID}"
: "${REGION:?Set REGION}"
: "${IMAGE_URI:?Set IMAGE_URI}"
: "${SERVICE_ACCOUNT:?Set SERVICE_ACCOUNT}"

JOB_NAME="${1:?Usage: run-job.sh JOB_NAME COMMAND [ARG...]}"
shift

COMMAND="${1:?Usage: run-job.sh JOB_NAME COMMAND [ARG...]}"
shift || true

JOB_MEMORY="${JOB_MEMORY:-512Mi}"
JOB_CPU="${JOB_CPU:-1}"
JOB_TIMEOUT="${JOB_TIMEOUT:-900s}"
JOB_MAX_RETRIES="${JOB_MAX_RETRIES:-1}"
EXECUTE_JOB="${EXECUTE_JOB:-true}"

deploy_args=(
  run
  jobs
  deploy
  "${JOB_NAME}"
  --project "${PROJECT_ID}"
  --region "${REGION}"
  --image "${IMAGE_URI}"
  --service-account "${SERVICE_ACCOUNT}"
  --memory "${JOB_MEMORY}"
  --cpu "${JOB_CPU}"
  --task-timeout "${JOB_TIMEOUT}"
  --max-retries "${JOB_MAX_RETRIES}"
  --command "${COMMAND}"
)

if [[ "$#" -gt 0 ]]; then
  deploy_args+=(--args "$(IFS=,; echo "$*")")
fi

if [[ -n "${ENV_VARS_FILE:-}" ]]; then
  deploy_args+=(--env-vars-file "${ENV_VARS_FILE}")
fi

if [[ -n "${SECRETS_SPEC:-}" ]]; then
  deploy_args+=(--set-secrets "${SECRETS_SPEC}")
fi

if [[ -n "${CLOUD_SQL_CONNECTION_NAME:-}" ]]; then
  deploy_args+=(--set-cloudsql-instances "${CLOUD_SQL_CONNECTION_NAME}")
fi

gcloud "${deploy_args[@]}"

if [[ "${EXECUTE_JOB}" == "true" ]]; then
  gcloud run jobs execute "${JOB_NAME}" --project "${PROJECT_ID}" --region "${REGION}" --wait
fi
