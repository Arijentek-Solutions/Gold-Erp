# Desktop Icons, Apps Screen, and Shortcuts Fix

## Problem
- Other apps (CRM, Helpdesk, Gameplan, Telephony, Insights) were not showing on the apps screen
- Desktop icons were missing
- Shortcuts were not appearing

## Root Cause
1. Desktop icons are stored as JSON files in each app but must be **imported into the database** to appear
2. The `after_migrate` hook was only importing zevar_core's desktop icons, not all apps
3. Workspace shortcuts need to be created from workspaces

## Solution
Created a comprehensive fix in `zevar_core/fix_desktop_icons.py` that:

1. **Imports all desktop icons** from all installed apps (ERPNext, HRMS, Frappe, CRM, Helpdesk, etc.)
2. **Creates missing app icons** for apps that don't have desktop icons defined
3. **Creates workspace icons** from all available workspaces
4. **Verifies and fixes shortcuts** using the zevar_core shortcut seed

## How to Apply the Fix

### Option 1: Run the Patch (Recommended)
```bash
bench --site [site-name] migrate
```
The patch `zevar_core.patches.v1_0.import_all_desktop_icons` will run automatically.

### Option 2: Run the Bench Command
```bash
bench --site [site-name] fix-desktop-icons
```

### Option 3: Run in Python Console
```bash
bench --site [site-name] console
```
```python
from zevar_core.fix_desktop_icons import execute
execute()
```

## Files Changed
- `zevar_core/fix_desktop_icons.py` - Main fix script
- `zevar_core/patches/v1_0/import_all_desktop_icons.py` - Migration patch
- `zevar_core/patches.txt` - Added patch registration
- `zevar_core/hooks.py` - Added after_migrate hook
- `zevar_core/commands.py` - Added bench command
- `zevar_core/commands/fix_desktop.py` - Bench command implementation

## After Applying the Fix
1. Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
2. Refresh the page
3. All apps should now appear on the apps screen
4. Desktop icons should be visible
5. Shortcuts should be available

## Expected Results
After the fix, you should see:
- **Frappe** - Framework, System, Website, etc.
- **ERPNext** - Accounting, Selling, Stock, Manufacturing, etc.
- **HRMS** - HR, Payroll, Leaves, etc.
- **CRM** - Frappe CRM
- **Helpdesk** - Helpdesk
- **Gameplan** - Gameplan
- **Zevar POS** - Zevar POS (custom)
- **Insights** - Insights (if installed)

## Troubleshooting
If icons still don't appear after the fix:

1. **Clear cache:**
   ```bash
   bench --site [site-name] clear-cache
   ```

2. **Restart services:**
   ```bash
   bench restart
   ```

3. **Check desktop icons in database:**
   ```bash
   bench --site [site-name] mariadb
   ```
   ```sql
   SELECT name, label, icon_type, app FROM `tabDesktop Icon`;
   ```

4. **Check user permissions:**
   - Desktop icons are filtered by user permissions
   - Ensure user has roles that allow viewing the icons

## Notes
- Desktop icons are cached per user - clearing cache is important
- The fix runs automatically on future migrations via `after_migrate` hook
- Custom desktop icons created by users are preserved
