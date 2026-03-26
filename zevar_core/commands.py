"""Bench command registrations for Zevar Core."""

from zevar_core.migration.commands import import_legacy_data, show_mapping_info

commands = [import_legacy_data, show_mapping_info]
