# FoxPro Migration Local Setup

## What Was Done

The FoxPro migration code was already present in the `zevar_core` app, so the best path was to finish the local wiring instead of duplicating files.

I made these changes:

1. Added `dbfread` to [`pyproject.toml`](/workspace/development/frappe-bench/apps/zevar_core/pyproject.toml) so the FoxPro reader installs with the app.
2. Added [`zevar_core/commands.py`](/workspace/development/frappe-bench/apps/zevar_core/zevar_core/commands.py) so Bench v16 can discover `zevar-import-legacy` and `zevar-mapping-info`.
3. Updated [`zevar_core/migration/commands.py`](/workspace/development/frappe-bench/apps/zevar_core/zevar_core/migration/commands.py) so the backup path is optional and auto-resolves from:
   - site config `zevar_legacy_backup_path`
   - `~/Downloads/Zevar_HIPmall_RD`
   - `/workspace/development/Zevar_URMS/Zevar_HIPmall_RD/Zevar_HIPmall_RD`
   - `/Zevar_URMS/Zevar_HIPmall_RD`
4. Added [`scripts/setup_migration_local.sh`](/workspace/development/frappe-bench/apps/zevar_core/scripts/setup_migration_local.sh) to install dependencies and save the backup path to site config.

## Backup Paths

- Local machine path provided by user: `~/Downloads/Zevar_HIPmall_RD`
- Workspace path detected during setup: `/workspace/development/Zevar_URMS/Zevar_HIPmall_RD/Zevar_HIPmall_RD`

## How To Run It

From [`frappe-bench/apps/zevar_core`](/workspace/development/frappe-bench/apps/zevar_core):

```bash
./scripts/setup_migration_local.sh zevar.localhost ~/Downloads/Zevar_HIPmall_RD
```

Then from [`frappe-bench`](/workspace/development/frappe-bench):

```bash
bench --site zevar.localhost zevar-mapping-info
bench --site zevar.localhost zevar-import-legacy --dry-run
bench --site zevar.localhost zevar-import-legacy
```

## Notes

- `--dry-run` is the safe verification step and does not create records.
- If the local `~/Downloads` path is not present, the setup script falls back to the workspace FoxPro backup path when available.
- Bench command discovery on this setup comes from `zevar_core.commands`, not `hooks.py`.

## Verification

Validated on `2026-03-19` against `/workspace/development/Zevar_URMS/Zevar_HIPmall_RD/Zevar_HIPmall_RD` with:

```bash
bench --site zevar.localhost zevar-mapping-info
bench --site zevar.localhost zevar-import-legacy --dry-run
```

Dry-run summary:

- `Store Location`: total `927`, imported `1`, skipped `926`
- `Employee`: total `2092`, imported `2092`, skipped `0`
- `Customer`: no matching `Guest*.bup/.dbf` file detected
- `Item`: `INVENTRY.DBF` exists but currently contains `0` rows
- `Jewelry Appraisal`: `1APTERM1.DBF` exists but currently contains `0` rows
