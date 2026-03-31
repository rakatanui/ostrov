#!/usr/bin/env bash
set -euo pipefail

TEMPLATE_FILE="${1:-cloudrun.production.env.yaml}"
OUTPUT_FILE="${2:-cloudrun.production.rendered.env.yaml}"

: "${GOOGLE_CLOUD_PROJECT:?Set GOOGLE_CLOUD_PROJECT}"
: "${CLOUD_SQL_CONNECTION_NAME:?Set CLOUD_SQL_CONNECTION_NAME}"
: "${GCS_STATIC_BUCKET_NAME:?Set GCS_STATIC_BUCKET_NAME}"
: "${GCS_MEDIA_BUCKET_NAME:?Set GCS_MEDIA_BUCKET_NAME}"

sed \
  -e "s|__GOOGLE_CLOUD_PROJECT__|${GOOGLE_CLOUD_PROJECT}|g" \
  -e "s|__CLOUD_SQL_CONNECTION_NAME__|${CLOUD_SQL_CONNECTION_NAME}|g" \
  -e "s|__GCS_STATIC_BUCKET_NAME__|${GCS_STATIC_BUCKET_NAME}|g" \
  -e "s|__GCS_MEDIA_BUCKET_NAME__|${GCS_MEDIA_BUCKET_NAME}|g" \
  "${TEMPLATE_FILE}" > "${OUTPUT_FILE}"

if grep -n "__[A-Z0-9_][A-Z0-9_]*__" "${OUTPUT_FILE}" >/dev/null; then
  echo "Unresolved placeholders remain in ${OUTPUT_FILE}." >&2
  exit 1
fi

printf 'Rendered env vars file: %s\n' "${OUTPUT_FILE}"
