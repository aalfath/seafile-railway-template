#!/bin/bash
# Start Seafile on Railway: fixed settings get defaults here, so the template only carries
# references, generated secrets and the admin email.
set -euo pipefail

export SEAFILE_SERVER_PROTOCOL="${SEAFILE_SERVER_PROTOCOL:-https}"
export SEAFILE_MYSQL_DB_PORT="${SEAFILE_MYSQL_DB_PORT:-3306}"
export SEAFILE_MYSQL_DB_USER="${SEAFILE_MYSQL_DB_USER:-seafile}"
export SEAFILE_MYSQL_DB_CCNET_DB_NAME="${SEAFILE_MYSQL_DB_CCNET_DB_NAME:-ccnet_db}"
export SEAFILE_MYSQL_DB_SEAFILE_DB_NAME="${SEAFILE_MYSQL_DB_SEAFILE_DB_NAME:-seafile_db}"
export SEAFILE_MYSQL_DB_SEAHUB_DB_NAME="${SEAFILE_MYSQL_DB_SEAHUB_DB_NAME:-seahub_db}"
export CACHE_PROVIDER="${CACHE_PROVIDER:-redis}"
export REDIS_PORT="${REDIS_PORT:-6379}"
export TIME_ZONE="${TIME_ZONE:-Etc/UTC}"
export SITE_ROOT="${SITE_ROOT:-/}"
export NON_ROOT="${NON_ROOT:-false}"
export ENABLE_GO_FILESERVER="${ENABLE_GO_FILESERVER:-true}"
export SEAFILE_LOG_TO_STDOUT="${SEAFILE_LOG_TO_STDOUT:-true}"
# Optional add-ons that need their own services are off unless you deploy them.
export ENABLE_SEADOC="${ENABLE_SEADOC:-false}"
export ENABLE_NOTIFICATION_SERVER="${ENABLE_NOTIFICATION_SERVER:-false}"
export ENABLE_SEAFILE_AI="${ENABLE_SEAFILE_AI:-false}"

: "${SEAFILE_SERVER_HOSTNAME:?SEAFILE_SERVER_HOSTNAME is required (the public domain)}"
: "${SEAFILE_MYSQL_DB_HOST:?SEAFILE_MYSQL_DB_HOST is required}"
: "${SEAFILE_MYSQL_DB_PASSWORD:?SEAFILE_MYSQL_DB_PASSWORD is required}"
: "${JWT_PRIVATE_KEY:?JWT_PRIVATE_KEY is required}"

# First start only: Seafile creates its databases with the MariaDB root password and the
# first admin account. Refuse to start with the image's default admin (me@example.com / asecret).
if [ ! -e /shared/seafile/seafile-data ]; then
  if [ -z "${INIT_SEAFILE_ADMIN_EMAIL:-}" ] || [ -z "${INIT_SEAFILE_ADMIN_PASSWORD:-}" ]; then
    echo "railway-start: set INIT_SEAFILE_ADMIN_EMAIL and INIT_SEAFILE_ADMIN_PASSWORD before the first start" >&2
    exit 1
  fi
  : "${INIT_SEAFILE_MYSQL_ROOT_PASSWORD:?INIT_SEAFILE_MYSQL_ROOT_PASSWORD is required on the first start}"
fi
# Recover from a first start that was interrupted halfway (see railway-init-guard.py).
python3 /usr/local/bin/railway-init-guard.py

exec /sbin/my_init -- /scripts/enterpoint.sh
