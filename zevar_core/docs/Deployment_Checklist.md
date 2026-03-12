# Zevar POS v1.0.0 - Deployment Checklist

**Release Date:** March 2026
**Version:** 1.0.0

---

## Pre-Deployment Checklist

### Environment Requirements

- [ ] Frappe Framework v14+ installed
- [ ] ERPNext v14+ installed
- [ ] Python 3.10+ available
- [ ] Node.js 18+ available
- [ ] MariaDB 10.6+ running
- [ ] Redis server running
- [ ] SSL certificate configured (production)

### Database Preparation

- [ ] Database backup taken
- [ ] Database size verified (< 10GB recommended)
- [ ] Database indexes optimized
- [ ] Database user permissions verified

### File System

- [ ] Sufficient disk space (> 50GB recommended)
- [ ] File permissions correct (frappe user owns files)
- [ ] Backup directory configured
- [ ] Log rotation configured

---

## Deployment Steps

### Step 1: Backup

```bash
# Full backup
bench --site your-site backup --with-files

# Verify backup
ls -la ~/frappe-bench/sites/your-site/private/backups/
```

### Step 2: Get Latest Code

```bash
cd ~/frappe-bench/apps/zevar_core
git fetch origin
git checkout v1.0.0
```

### Step 3: Run Migrations

```bash
bench --site your-site migrate
```

### Step 4: Clear Cache

```bash
bench --site your-site clear-cache
```

### Step 5: Build Assets

```bash
bench build --app zevar_core
```

### Step 6: Restart Services

```bash
bench restart
```

### Step 7: Verify Deployment

- [ ] Site loads without errors
- [ ] Login works
- [ ] POS terminal accessible
- [ ] Employee portal accessible
- [ ] API endpoints respond

---

## Post-Deployment Verification

### Core Functionality Tests

#### POS Terminal
- [ ] POS profile selector works
- [ ] Item search returns results
- [ ] Cart operations work (add/remove/modify)
- [ ] Checkout completes successfully
- [ ] Receipt prints correctly

#### Register Operations
- [ ] Open register creates session
- [ ] Close register calculates correctly
- [ ] Variance is detected and logged

#### Payments
- [ ] Cash payment processes
- [ ] Card payment processes
- [ ] Split payment works
- [ ] Gift card redemption works
- [ ] Trade-in credit applies

#### Special Transactions
- [ ] Layaway creation works
- [ ] Return processing works
- [ ] Void with manager approval works

#### Reports
- [ ] Sales by Salesperson generates
- [ ] Hourly Sales generates
- [ ] Payment Summary generates
- [ ] Layaway Aging generates
- [ ] Trade-In Summary generates

### Security Verification

- [ ] All API endpoints require authentication
- [ ] Manager override requires PIN
- [ ] Audit logs are being created
- [ ] Permission checks work

### Performance Verification

- [ ] Page load < 3 seconds
- [ ] API response < 500ms
- [ ] Search results < 1 second
- [ ] Report generation < 10 seconds

---

## Rollback Procedure

If deployment fails:

```bash
# Restore backup
bench --site your-site restore ~/frappe-bench/sites/your-site/private/backups/backup-file.sql.gz

# Revert code
cd ~/frappe-bench/apps/zevar_core
git checkout previous-version

# Rebuild
bench build --app zevar_core
bench restart
```

---

## Monitoring Setup

### Health Checks

```bash
# Check if services are running
bench doctor

# Check scheduler
bench scheduler-status

# Check workers
bench worker-status
```

### Log Monitoring

```bash
# Watch error logs
tail -f ~/frappe-bench/logs/bench-start.log

# Watch scheduler logs
tail -f ~/frappe-bench/logs/bench-schedule.log
```

### Alerts to Configure

- [ ] Database connection failures
- [ ] High CPU usage
- [ ] High memory usage
- [ ] Disk space low
- [ ] SSL certificate expiry

---

## Production Configuration

### Recommended Settings

```json
// site_config.json
{
    "db_name": "your-site",
    "db_password": "secure-password",
    "developer_mode": 0,
    "disable_session_cache": 0,
    "max_file_size": 10485760,
    "session_timeout": 28800,
    "force_ssl": true
}
```

### Performance Tuning

```bash
# Increase worker count
bench config worker-count 4

# Enable gunicorn workers
bench config gunicorn-workers 4

# Set timeout
bench config timeout 120
```

### Security Hardening

- [ ] Change default admin password
- [ ] Disable developer mode
- [ ] Enable SSL
- [ ] Configure firewall rules
- [ ] Set up fail2ban
- [ ] Enable rate limiting

---

## Support Contacts

| Issue | Contact |
|-------|---------|
| Application Bugs | support@zevar.com |
| Infrastructure | devops@zevar.com |
| Emergency | +1-XXX-XXX-XXXX |

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| QA Lead | | | |
| Operations | | | |
| Product Owner | | | |

---

*Deployment completed: _______________*
