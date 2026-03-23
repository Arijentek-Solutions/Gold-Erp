#!/bin/sh

set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
APP_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
BENCH_ROOT=$(CDPATH= cd -- "$APP_ROOT/../.." && pwd)

SITE="${1:-zevar.localhost}"
BACKUP_PATH="${2:-$HOME/Downloads/Zevar_HIPmall_RD}"

if [ ! -d "$BENCH_ROOT" ] || [ ! -x "$BENCH_ROOT/env/bin/python" ]; then
	echo "Bench root not found from $APP_ROOT" >&2
	exit 1
fi

if [ ! -d "$BACKUP_PATH" ]; then
	for candidate in \
		"/workspace/development/Zevar_URMS/Zevar_HIPmall_RD/Zevar_HIPmall_RD" \
		"/Zevar_URMS/Zevar_HIPmall_RD"
	do
		if [ -d "$candidate" ]; then
			BACKUP_PATH="$candidate"
			break
		fi
	done
fi

cd "$BENCH_ROOT"

echo "Using site: $SITE"
echo "Using backup path: $BACKUP_PATH"

echo "Installing Zevar Core Python dependencies..."
./env/bin/pip install -e apps/zevar_core

echo "Saving backup path to site config..."
bench --site "$SITE" set-config zevar_legacy_backup_path "$BACKUP_PATH"

echo "Migration setup complete."
echo "Next steps:"
echo "  bench --site \"$SITE\" zevar-mapping-info"
echo "  bench --site \"$SITE\" zevar-import-legacy --dry-run"
echo "  bench --site \"$SITE\" zevar-import-legacy"
