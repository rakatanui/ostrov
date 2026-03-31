#!/usr/bin/env bash
set -euo pipefail

: "${PROJECT_ID:?Set PROJECT_ID}"
: "${REGION:?Set REGION}"
: "${REPOSITORY:?Set REPOSITORY}"

IMAGE_NAME="${IMAGE_NAME:-ostrov-quest-web}"
IMAGE_TAG="${IMAGE_TAG:-$(date +%Y%m%d-%H%M%S)}"
IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${IMAGE_NAME}:${IMAGE_TAG}"

gcloud builds submit \
  --project "${PROJECT_ID}" \
  --config cloudbuild.image.yaml \
  --substitutions "_IMAGE_URI=${IMAGE_URI}" \
  .

printf 'Built image: %s\n' "${IMAGE_URI}"
