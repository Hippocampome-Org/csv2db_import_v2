#!/usr/bin/env bash
# Back up only the disposable staging HC database. Credentials stay outside Git.
set -euo pipefail
if [[ "${1:---plan}" != "--execute-staging" ]]; then
  printf '%s\n' 'PLAN: read-only dump of HC from hippocampome-mysql-staging; no database command executed.'
  printf '%s\n' 'To execute, provide HC_MYSQL_DEFAULTS_FILE (private MySQL client configuration) and HC_BACKUP_DIR outside the web root.'
  exit 0
fi
: "${HC_MYSQL_DEFAULTS_FILE:?Set the private MySQL client defaults file}"
: "${HC_BACKUP_DIR:?Set a private backup directory outside the web root}"
[[ -f "$HC_MYSQL_DEFAULTS_FILE" && ! -L "$HC_MYSQL_DEFAULTS_FILE" ]] || exit 1
mode=$(stat -c '%a' "$HC_MYSQL_DEFAULTS_FILE")
[[ "$mode" == 600 || "$mode" == 400 ]] || { printf '%s\n' 'Client configuration must have mode 600 or 400.' >&2; exit 1; }
backup=$(realpath -m "$HC_BACKUP_DIR")
case "$backup" in /var/www/*|/data/hippocampome-staging/production-layout|/data/hippocampome-staging/production-layout/*|/data/hippocampome-staging/php83-dev|/data/hippocampome-staging/php83-dev/*|/data/hippocampome-staging/www|/data/hippocampome-staging/www/*) printf '%s\n' 'Refusing a backup directory under a website source tree.' >&2; exit 1;; esac
umask 077
mkdir -p "$backup"
out="$backup/HC-$(date -u +%Y%m%dT%H%M%SZ).sql"
[[ ! -e "$out" ]] || exit 1
docker exec -i hippocampome-mysql-staging mysqldump --defaults-extra-file=/dev/stdin --single-transaction --skip-lock-tables HC < "$HC_MYSQL_DEFAULTS_FILE" > "$out"
printf 'Staging backup written to %s\n' "$out"
