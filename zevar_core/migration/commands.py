"""
Bench Commands for Zevar Migration

Usage:
    bench --site <site> zevar-import-legacy /path/to/backup [--dry-run]
    bench --site <site> zevar-mapping-info
"""

import json
import frappe
from frappe.commands import pass_context
import click

from .foxpro_import import import_all, get_mapping_info


@click.command("zevar-import-legacy")
@click.argument("backup_path", required=True)
@click.option("--dry-run", is_flag=True, default=False, help="Preview import without creating records")
@click.option("--json-output", is_flag=True, default=False, help="Output results as JSON")
@pass_context
def import_legacy_data(context, backup_path, dry_run=False, json_output=False):
	"""
	Import legacy FoxPro data into Zevar.

	Import jewelry inventory, appraisals, employees, customers, and stores
	from Visual FoxPro backup files.

	Example:
	    bench --site hipmall.zevar zevar-import-legacy /path/to/Zevar_HIPmall_RD
	    bench --site hipmall.zevar zevar-import-legacy /path/to/backup --dry-run
	"""
	site = context.obj.get("site")

	if not site:
		click.echo("Please specify a site with --site")
		return

	frappe.init(site=site)
	frappe.connect()

	try:
		click.echo(f"\n{'[DRY RUN] ' if dry_run else ''}Importing legacy data from: {backup_path}")
		click.echo("-" * 60)

		results = import_all(backup_path, dry_run=dry_run)

		if json_output:
			click.echo(json.dumps(results, indent=2, default=str))
		else:
			# Print summary
			for category in ["stores", "employees", "customers", "inventory", "appraisals"]:
				stats = results.get(category, {})
				doctype = {
					"stores": "Store Location",
					"employees": "Employee",
					"customers": "Customer",
					"inventory": "Item",
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
	site = context.obj.get("site")

	if not site:
		click.echo("Please specify a site with --site")
		return

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
		click.echo("  bench --site <site> zevar-import-legacy /path/to/backup")
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
	return frappe.conf.get("zevar_legacy_backup_path", "/Zevar_URMS/Zevar_HIPmall_RD")


commands = [
	import_legacy_data,
	show_mapping_info,
]
