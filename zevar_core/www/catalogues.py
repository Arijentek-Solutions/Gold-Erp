"""Context for Catalogues www page."""

import frappe


def get_context(context):
	"""Set no_cache for the Catalogues page."""
	context.no_cache = 1
