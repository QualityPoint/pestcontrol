# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class WebsiteContactMessage(Document):
	def after_insert(self):
		notify_email = frappe.db.get_single_value("PC Website Settings", "email")
		if not notify_email:
			return

		# Queued (not `now=True`) so a broken/unconfigured mail server never
		# blocks or breaks the guest's actual form submission — capturing the
		# message always has to succeed regardless of whether the alert does.
		try:
			frappe.sendmail(
				recipients=[notify_email],
				subject=f"New website contact message from {self.full_name}",
				message=frappe.render_template(
					"""
					<p><b>Name:</b> {{ doc.full_name }}</p>
					<p><b>Email:</b> {{ doc.email }}</p>
					<p><b>Phone:</b> {{ doc.phone or "-" }}</p>
					<p><b>Message:</b></p>
					<p>{{ (doc.message or "").replace("\\n", "<br>") }}</p>
					""",
					{"doc": self},
				),
				reference_doctype=self.doctype,
				reference_name=self.name,
			)
		except Exception:
			frappe.log_error(title="Failed to queue contact message alert email")
			# frappe.throw()/msgprint() inside sendmail() already queued a
			# message (e.g. "no outgoing email account configured") before
			# raising — clear it so it doesn't leak into the guest's API
			# response; the form submission itself must look unaffected.
			frappe.clear_messages()
