"""Context for Employee Portal www page."""
import frappe

def get_context(context):
	"""Set no_cache for the portal page."""
	context.no_cache = 1
