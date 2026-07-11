#!/usr/bin/env bash
# Self-provisioning deploy for Paw Paw Land (adapted from ../Gulpac/scripts/deploy.sh).
# Packages the project, uploads it, installs system deps, builds assets, runs
# migrations, and wires up Gunicorn (systemd) behind Nginx on $PORT.
#
# Usage:
#   scripts/deploy.sh
#   PORT=8014 SERVER_NAME=example.com scripts/deploy.sh
set -Eeuo pipefail

REMOTE_USER="${REMOTE_USER:-root}"
REMOTE_HOST="${REMOTE_HOST:-168.144.92.215}"
APP_DIR="${APP_DIR:-/var/www/pawpawland}"
SERVICE_NAME="${SERVICE_NAME:-pawpawland}"
PORT="${PORT:-8014}"
SERVER_NAME="${SERVER_NAME:-$REMOTE_HOST}"
DJANGO_ALLOWED_HOSTS="${DJANGO_ALLOWED_HOSTS:-$SERVER_NAME,127.0.0.1,localhost}"
GUNICORN_WORKERS="${GUNICORN_WORKERS:-3}"
CLIENT_MAX_BODY_SIZE="${CLIENT_MAX_BODY_SIZE:-25M}"
SEED_DEMO="${SEED_DEMO:-1}"

REMOTE="${REMOTE_USER}@${REMOTE_HOST}"
ARCHIVE_NAME="pawpawland-deploy.tar.gz"
REMOTE_ARCHIVE="/tmp/${ARCHIVE_NAME}"
LOCAL_ARCHIVE="$(mktemp -t pawpawland-deploy.XXXXXX.tar.gz)"

cleanup() {
  rm -f "$LOCAL_ARCHIVE"
}
trap cleanup EXIT

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

quote_remote() {
  printf "%q" "$1"
}

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

require_cmd ssh
require_cmd scp
require_cmd tar

echo "Packaging project from $ROOT_DIR"
tar \
  --exclude-vcs \
  --exclude='./.git' \
  --exclude='*/.git' \
  --exclude='./.claude' \
  --exclude='./.venv' \
  --exclude='./venv' \
  --exclude='./node_modules' \
  --exclude='./db.sqlite3' \
  --exclude='./media' \
  --exclude='./staticfiles' \
  --exclude='./.env' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  --exclude='./.pytest_cache' \
  --exclude='./.ruff_cache' \
  -czf "$LOCAL_ARCHIVE" .

echo "Uploading archive to $REMOTE:$REMOTE_ARCHIVE"
scp "$LOCAL_ARCHIVE" "$REMOTE:$REMOTE_ARCHIVE"

echo "Deploying on $REMOTE"
ssh "$REMOTE" \
  "APP_DIR=$(quote_remote "$APP_DIR") SERVICE_NAME=$(quote_remote "$SERVICE_NAME") PORT=$(quote_remote "$PORT") SERVER_NAME=$(quote_remote "$SERVER_NAME") DJANGO_ALLOWED_HOSTS=$(quote_remote "$DJANGO_ALLOWED_HOSTS") GUNICORN_WORKERS=$(quote_remote "$GUNICORN_WORKERS") CLIENT_MAX_BODY_SIZE=$(quote_remote "$CLIENT_MAX_BODY_SIZE") SEED_DEMO=$(quote_remote "$SEED_DEMO") REMOTE_ARCHIVE=$(quote_remote "$REMOTE_ARCHIVE") bash -s" <<'REMOTE_SCRIPT'
set -Eeuo pipefail

if [[ "$(id -u)" -eq 0 ]]; then
  SUDO=""
else
  SUDO="sudo"
fi

case "$APP_DIR" in
  /opt/*|/srv/*|/var/www/*) ;;
  *)
    echo "Refusing to deploy outside /opt, /srv, or /var/www: $APP_DIR" >&2
    exit 1
    ;;
esac

ensure_env_value() {
  local key="$1"
  local value="$2"
  local file="$APP_DIR/.env"

  if $SUDO grep -q "^${key}=" "$file"; then
    $SUDO sed -i "s|^${key}=.*|${key}=${value}|" "$file"
  else
    echo "${key}=${value}" | $SUDO tee -a "$file" >/dev/null
  fi
}

stop_legacy_runserver() {
  if ! command -v ss >/dev/null 2>&1; then
    return
  fi

  local pids
  pids="$(ss -ltnp "sport = :${PORT}" 2>/dev/null | sed -n 's/.*pid=\([0-9]\+\).*/\1/p' | sort -u)"
  for pid in $pids; do
    local cmdline
    cmdline="$(tr '\0' ' ' < "/proc/${pid}/cmdline" 2>/dev/null || true)"
    if [[ "$cmdline" == *"manage.py runserver"* ]]; then
      echo "Stopping legacy runserver process $pid"
      $SUDO kill "$pid"
    fi
  done
}

export DEBIAN_FRONTEND=noninteractive

echo "Installing required system packages"
$SUDO apt-get update
$SUDO apt-get install -y nginx python3-venv python3-pip build-essential curl
if ! command -v npm >/dev/null 2>&1; then
  $SUDO apt-get install -y nodejs npm
fi

echo "Preparing app directory: $APP_DIR"
$SUDO mkdir -p "$APP_DIR"
$SUDO find "$APP_DIR" -mindepth 1 -maxdepth 1 \
  ! -name '.env' \
  ! -name 'db.sqlite3' \
  ! -name 'media' \
  ! -name '.venv' \
  -exec rm -rf {} +

echo "Unpacking project"
$SUDO tar --no-same-owner -xzf "$REMOTE_ARCHIVE" -C "$APP_DIR"
$SUDO mkdir -p "$APP_DIR/media" "$APP_DIR/staticfiles"

if [[ ! -f "$APP_DIR/.env" ]]; then
  echo "Creating production .env"
  SECRET="$($SUDO python3 -c 'import secrets; print(secrets.token_urlsafe(64))')"
  CSRF_ORIGINS="http://${SERVER_NAME}:${PORT},https://${SERVER_NAME}:${PORT},http://127.0.0.1:${PORT},http://localhost:${PORT}"
  $SUDO tee "$APP_DIR/.env" >/dev/null <<EOF
DEBUG=False
SECRET_KEY=$SECRET
ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS=$CSRF_ORIGINS
DATABASE_URL=sqlite:///$APP_DIR/db.sqlite3
EOF
  $SUDO chmod 600 "$APP_DIR/.env"
else
  echo "Updating existing .env"
  CSRF_ORIGINS="http://${SERVER_NAME}:${PORT},https://${SERVER_NAME}:${PORT},http://127.0.0.1:${PORT},http://localhost:${PORT}"
  ensure_env_value "DEBUG" "False"
  ensure_env_value "ALLOWED_HOSTS" "$DJANGO_ALLOWED_HOSTS"
  ensure_env_value "CSRF_TRUSTED_ORIGINS" "$CSRF_ORIGINS"
  if ! $SUDO grep -q '^SECRET_KEY=' "$APP_DIR/.env"; then
    SECRET="$($SUDO python3 -c 'import secrets; print(secrets.token_urlsafe(64))')"
    ensure_env_value "SECRET_KEY" "$SECRET"
  fi
  if ! $SUDO grep -q '^DATABASE_URL=' "$APP_DIR/.env"; then
    ensure_env_value "DATABASE_URL" "sqlite:///$APP_DIR/db.sqlite3"
  fi
fi

echo "Installing Python dependencies"
if [[ ! -x "$APP_DIR/.venv/bin/python" ]]; then
  $SUDO python3 -m venv "$APP_DIR/.venv"
fi

cd "$APP_DIR"
$SUDO "$APP_DIR/.venv/bin/python" -m pip install --upgrade pip
$SUDO "$APP_DIR/.venv/bin/pip" install -r requirements.txt

echo "Installing Node dependencies and building assets"
$SUDO npm install
$SUDO npm run build

echo "Running migrations"
$SUDO "$APP_DIR/.venv/bin/python" manage.py migrate --noinput

if [[ "$SEED_DEMO" == "1" ]]; then
  echo "Seeding demo content (idempotent)"
  $SUDO "$APP_DIR/.venv/bin/python" manage.py seed_demo
fi

echo "Collecting static files"
$SUDO "$APP_DIR/.venv/bin/python" manage.py collectstatic --noinput --clear --ignore 'src/*'

echo "Writing systemd service"
$SUDO tee "/etc/systemd/system/${SERVICE_NAME}.service" >/dev/null <<EOF
[Unit]
Description=Paw Paw Land Django app
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
UMask=0007
ExecStart=$APP_DIR/.venv/bin/gunicorn --workers $GUNICORN_WORKERS --bind unix:/run/${SERVICE_NAME}.sock --umask 007 --access-logfile - --error-logfile - config.wsgi:application
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

echo "Writing Nginx site on port $PORT"
$SUDO tee "/etc/nginx/sites-available/${SERVICE_NAME}" >/dev/null <<EOF
server {
    listen $PORT;
    listen [::]:$PORT;
    server_name $SERVER_NAME _;

    client_max_body_size $CLIENT_MAX_BODY_SIZE;

    location /static/ {
        alias $APP_DIR/staticfiles/;
        access_log off;
        expires 30d;
    }

    location /media/ {
        alias $APP_DIR/media/;
        access_log off;
        expires 30d;
    }

    location / {
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
        proxy_pass http://unix:/run/${SERVICE_NAME}.sock;
    }
}
EOF

$SUDO ln -sf "/etc/nginx/sites-available/${SERVICE_NAME}" "/etc/nginx/sites-enabled/${SERVICE_NAME}"

echo "Restarting services"
stop_legacy_runserver
$SUDO systemctl daemon-reload
$SUDO systemctl enable --now "$SERVICE_NAME"
$SUDO systemctl restart "$SERVICE_NAME"
$SUDO nginx -t
$SUDO systemctl enable --now nginx
$SUDO systemctl restart nginx

echo "Opening firewall port $PORT"
if command -v ufw >/dev/null 2>&1; then
  $SUDO ufw allow "${PORT}/tcp" comment "$SERVICE_NAME" >/dev/null 2>&1 || true
else
  echo "UFW not installed; check cloud firewall rules if the port is closed"
fi

echo "Verifying deployment"
$SUDO "$APP_DIR/.venv/bin/python" manage.py check
curl -fsS --max-time 15 -o /dev/null "http://127.0.0.1:${PORT}"
systemctl is-active --quiet "$SERVICE_NAME"
systemctl is-active --quiet nginx

echo "Deployment complete: http://$SERVER_NAME:$PORT"
REMOTE_SCRIPT

echo "Checking public URL: http://${SERVER_NAME}:${PORT}"
if command -v curl >/dev/null 2>&1; then
  if curl -fsS --max-time 15 -o /dev/null "http://${SERVER_NAME}:${PORT}"; then
    echo "Public URL responded successfully"
  else
    echo "Public URL check failed; server deploy completed, but DNS/firewall may need attention" >&2
    exit 1
  fi
else
  echo "curl is not installed locally; skipping public URL check"
fi

echo "Done: http://${SERVER_NAME}:${PORT}"
