# Copyright (c) 2026, Zevar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now


class POSManagerOverride(Document):
	"""POS Manager Override for tracking approval requests."""

	def before_insert(self) -> None:
		"""Set default values before insert."""
		if not self.request_time:
			self.request_time = now()

	def validate(self) -> None:
		"""Validate the override request."""
		self._validate_status_transition()
		self._validate_approval_fields()

	def _validate_status_transition(self) -> None:
		"""Ensure valid status transitions."""
		if self.is_new():
			return

		old_doc = self.get_doc_before_save()
		if old_doc and old_doc.status != "Pending" and self.status != old_doc.status:
			frappe.throw(
				frappe._("Cannot change status from {0} to {1}").format(
					old_doc.status, self.status
				)
			)

	def _validate_approval_fields(self) -> None:
		"""Ensure approval fields are set when approved/rejected."""
		if self.status in ("Approved", "Rejected"):
			if not self.approved_by:
				frappe.throw(
					frappe._("Approved By is required when status is {0}").format(self.status)
				)
			if not self.approval_time:
				self.approval_time = now()

	def on_update(self) -> None:
		"""Log the override action."""
		if self.status in ("Approved", "Rejected") and self.has_value_changed("status"):
			self._log_audit_event()

	def _log_audit_event(self) -> None:
		"""Create audit log entry for the override."""
		try:
			audit_log = frappe.get_doc({
				"doctype": "POS Audit Log",
				"user": self.approved_by,
				"event_type": f"manager_override_{self.status.lower()}",
				"category": "Security",
				"severity": "Info",
				"timestamp": now(),
				"reference_type": "POS Manager Override",
				"reference_document": self.name,
				"details": f"Manager override request for '{self.action}' was {self.status.lower()}. Reason: {self.reason}"
			})
			audit_log.insert(ignore_permissions=True)
		except Exception:
			# Don't fail the main operation if audit logging fails
			frappe.log_error("Failed to create audit log for manager override")
