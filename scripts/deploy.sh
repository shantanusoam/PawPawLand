#!/usr/bin/env bash
# Deploy Paw Paw Land to a server running Nginx + systemd-managed Gunicorn.
#
# Usage:
#   scripts/deploy.sh
#   REMOTE_HOST=example.com SERVER_NAME=pawpawland.example.com scripts/deploy.sh
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-pawpawland.com.au}"
REMOTE_USER="${REMOTE_USER:-deploy}"
REMOTE_DIR="${REMOTE_DIR:-/srv/pawpawland}"
SERVER_NAME="${SERVER_NAME:-$REMOTE_HOST}"
SERVICE_NAME="${SERVICE_NAME:-pawpawland}"
PYTHON_BIN="${PYTHON_BIN:-python3.12}"

SSH_TARGET="${REMOTE_USER}@${REMOTE_HOST}"

echo "==> Deploying to ${SSH_TARGET}:${REMOTE_DIR} (server_name: ${SERVER_NAME})"

echo "==> Syncing code"
rsync -az --delete \
  --exclude '.git' \
  --exclude '.venv' \
  --exclude 'node_modules' \
  --exclude 'db.sqlite3' \
  --exclude 'media' \
  --exclude 'staticfiles' \
  --exclude '.env' \
  ./ "${SSH_TARGET}:${REMOTE_DIR}/"

echo "==> Installing dependencies and building"
ssh "$SSH_TARGET" bash -s <<EOF
set -euo pipefail
cd "${REMOTE_DIR}"

if [ ! -d .venv ]; then
  ${PYTHON_BIN} -m venv .venv
fi
.venv/bin/pip install -q -r requirements.txt

npm install --no-fund --no-audit
npm run build

.venv/bin/python manage.py migrate --noinput
.venv/bin/python manage.py collectstatic --noinput

sudo systemctl restart "${SERVICE_NAME}"
sudo nginx -t
sudo systemctl reload nginx
EOF

echo "==> Deployed https://${SERVER_NAME}"
