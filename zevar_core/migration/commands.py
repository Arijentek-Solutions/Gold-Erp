"""
Bench Commands for Zevar Migration

Usage:
    bench --site <site> zevar-import-legacy [/path/to/backup] [--dry-run]
    bench --site <site> zevar-mapping-info
"""

import json
import os

import frappe
from frappe.commands import get_site, pass_context
import click

from .foxpro_import import import_all, get_mapping_info


DEFAULT_LEGACY_BACKUP_PATHS = (
	"/workspace/development/Zevar_URMS/Zevar_HIPmall_MD_1",
	"~/Downloads/Zevar_HIPmall_RD",
	"/workspace/development/Zevar_URMS/Zevar_HIPmall_RD/Zevar_HIPmall_RD",
	"/Zevar_URMS/Zevar_HIPmall_RD",
)


def resolve_legacy_backup_path(backup_path: str | None = None) -> str:
	"""Resolve the best available legacy backup path."""
	candidate_paths: list[str] = []

	if backup_path:
		candidate_paths.append(backup_path)

	configured_path = frappe.conf.get("zevar_legacy_backup_path")
	if configured_path:
		candidate_paths.append(configured_path)

	candidate_paths.extend(DEFAULT_LEGACY_BACKUP_PATHS)

	expanded_paths: list[str] = []
	for path in candidate_paths:
		expanded_path = os.path.abspath(os.path.expanduser(path))
		if expanded_path not in expanded_paths:
			expanded_paths.append(expanded_path)

	for path in expanded_paths:
		if os.path.isdir(path):
			return path

	return expanded_paths[0]


@click.command("zevar-import-legacy")
@click.argument("backup_path", required=False)
@click.option("--dry-run", is_flag=True, default=False, help="Preview import without creating records")
@click.option("--json-output", is_flag=True, default=False, help="Output results as JSON")
@click.option("--skip-transactions", is_flag=True, default=False, help="Skip Sales Invoice import (slow)")
@pass_context
def import_legacy_data(context, backup_path, dry_run=False, json_output=False, skip_transactions=False):
	"""
	Import legacy FoxPro data into Zevar.

	Import jewelry inventory, appraisals, employees, customers, and stores
	from Visual FoxPro backup files.

	Example:
	    bench --site hipmall.zevar zevar-import-legacy /path/to/Zevar_HIPmall_RD
	    bench --site hipmall.zevar zevar-import-legacy --dry-run
	    bench --site hipmall.zevar zevar-import-legacy --skip-transactions
	"""
	site = get_site(context)

	frappe.init(site=site)
	frappe.connect()

	try:
		resolved_backup_path = resolve_legacy_backup_path(backup_path)
		click.echo(f"\n{'[DRY RUN] ' if dry_run else ''}Importing legacy data from: {resolved_backup_path}")
		click.echo("-" * 60)

		results = import_all(resolved_backup_path, dry_run=dry_run, skip_transactions=skip_transactions)

		if json_output:
			click.echo(json.dumps(results, indent=2, default=str))
		else:
			# Print summary
			for category in [
				"stores",
				"employees",
				"categories",
				"item_attributes",
				"purities",
				"suppliers",
				"customers",
				"inventory",
				"repair_types",
				"gold_rates",
				"transactions",
				"appraisals",
			]:
				stats = results.get(category, {})
				doctype = {
					"stores": "Store Location",
					"employees": "Employee",
					"categories": "Item Group",
					"item_attributes": "Item Attribute (Color/Clarity)",
					"purities": "Zevar Purity",
					"suppliers": "Supplier",
					"customers": "Customer",
					"inventory": "Item",
					"repair_types": "Repair Type",
					"gold_rates": "Gold Rate Log",
					"transactions": "Sales Invoice",
					"appraisals": "Jewelry Appraisal",
				}.get(category)

				click.echo(f"\n{doctype}:")
				click.echo(f"  Total: {stats.get('total', 0)}")
				click.echo(f"  Imported: {stats.get('imported', 0)}")
				click.echo(f"  Skipped: {stats.get('skipped', 0)}")
				if stats.get("errors"):
					click.echo(f"  Errors: {len(stats.get('errors', []))}")
					for error in stats.get("errors", [])[:5]:
						click.echo(f"    - {error}")

			click.echo("\n" + "=" * 60)
			click.echo(f"Total Records: {results.get('total_records', 0)}")
			click.echo(f"Total Imported: {results.get('total_imported', 0)}")
			click.echo(f"Total Skipped: {results.get('total_skipped', 0)}")
			click.echo(f"Total Errors: {results.get('total_errors', 0)}")

			if dry_run:
				click.echo("\n[DRY RUN] No records were actually created.")
				click.echo("Run without --dry-run to import data.")

	finally:
		frappe.destroy()


@click.command("zevar-mapping-info")
@pass_context
def show_mapping_info(context):
	"""
	Show field mapping information for legacy data import.

	Displays how legacy FoxPro fields map to Zevar DocType fields.

	Example:
	    bench --site hipmall.zevar zevar-mapping-info
	"""
	site = get_site(context)

	frappe.init(site=site)
	frappe.connect()

	try:
		mappings = get_mapping_info()

		click.echo("\n" + "=" * 60)
		click.echo("Zevar Legacy Data Import - Field Mappings")
		click.echo("=" * 60)

		for category, info in mappings.items():
			click.echo(f"\n{info['doctype']} ({info['file']}):")
			click.echo("-" * 40)
			for legacy, zevar in info["fields"].items():
				click.echo(f"  {legacy:20} → {zevar}")

		click.echo("\n" + "=" * 60)
		click.echo("Usage:")
		click.echo("  bench --site <site> zevar-import-legacy")
		click.echo("  bench --site <site> zevar-import-legacy /path/to/backup --dry-run")
		click.echo("")

	finally:
		frappe.destroy()


def get_legacy_backup_path():
	"""
	Get the default legacy backup path.

	Can be configured in site_config.json as:
	    "zevar_legacy_backup_path": "/path/to/backup"
	"""
	return resolve_legacy_backup_path()


commands = [
	import_legacy_data,
	show_mapping_info,
]
