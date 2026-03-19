"""
Zevar Core Data Migration Module

This module provides utilities for importing legacy data from
Visual FoxPro (DBF) format into Zevar DocTypes.

Main Components:
- foxpro_import: DBF file parser and field mappers
- commands: Bench commands for running migrations

Usage:
    bench --site <site> zevar-import-legacy /path/to/backup
    bench --site <site> zevar-mapping-info
"""

from .foxpro_import import (
	import_all,
	import_appraisals,
	import_inventory,
	import_employees,
	import_customers,
	import_stores,
	get_mapping_info,
)
from .commands import get_legacy_backup_path

__all__ = [
	"import_all",
	"import_appraisals",
	"import_inventory",
	"import_employees",
	"import_customers",
	"import_stores",
	"get_mapping_info",
	"get_legacy_backup_path",
]
