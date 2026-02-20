"""Context for POS www page — resolves hashed Vite asset filenames."""

import os

import frappe


def get_context(context):
	"""Find the Vite-built JS/CSS assets and pass them to the template."""
	assets_dir = os.path.join(frappe.get_app_path("zevar_core"), "public", "pos", "assets")

	js_file = ""
	css_file = ""
	vendor_js = ""
	vendor_css = ""

	if os.path.isdir(assets_dir):
		for f in os.listdir(assets_dir):
			if f.startswith("index.") and f.endswith(".js"):
				js_file = f
			elif f.startswith("index.") and f.endswith(".css"):
				css_file = f
			elif f.startswith("vendor.") and f.endswith(".js"):
				vendor_js = f
			elif f.startswith("vendor.") and f.endswith(".css"):
				vendor_css = f

	context.pos_js = f"/assets/zevar_core/pos/assets/{js_file}" if js_file else ""
	context.pos_css = f"/assets/zevar_core/pos/assets/{css_file}" if css_file else ""
	context.vendor_js = f"/assets/zevar_core/pos/assets/{vendor_js}" if vendor_js else ""
	context.vendor_css = f"/assets/zevar_core/pos/assets/{vendor_css}" if vendor_css else ""
	context.no_cache = 1
