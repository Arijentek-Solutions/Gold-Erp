"""
Trade-In validation hooks for Sales Invoice.
Enforces the strict 2x rule: new item value must be >= 2x trade-in value.
"""

import frappe
from frappe import _
from frappe.utils import flt


def validate_trade_in_2x_rule(doc, method=None):
	"""
	Run on Sales Invoice validate.
	For each trade-in row, enforce that the new item value is at least
	2x the trade-in value, unless a manager override is present.
	"""
	trade_ins = doc.get("custom_trade_ins")
	if not trade_ins:
		return

	for row in trade_ins:
		trade_in_value = flt(row.trade_in_value)
		new_item_value = flt(row.new_item_value)

		if trade_in_value <= 0:
			frappe.throw(_("Row {0}: Trade-in value must be greater than zero.").format(row.idx))

		minimum_new_value = trade_in_value * 2

		# Auto-compute the minimum for display
		row.minimum_new_value = minimum_new_value

		if new_item_value < minimum_new_value:
			# Set validation status
			row.upgrade_validation = "Override Required"

			if not row.manager_override:
				frappe.throw(
					_(
						"Row {0}: New item value (${1:,.2f}) must be at least 2x "
						"the trade-in value (minimum ${2:,.2f}). "
						"Requires Manager Override."
					).format(row.idx, new_item_value, minimum_new_value)
				)

			# Manager override present — allow but log the override
			if not row.override_reason:
				frappe.throw(
					_("Row {0}: Override reason is required when manager override is used.").format(row.idx)
				)
		else:
			row.upgrade_validation = "Valid"
