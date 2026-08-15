# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import escape_html


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
				# Reviewed: template string is a fixed literal, never derived
				# from user input, so this isn't template injection — only
				# field *values* are interpolated. Those values are still
				# HTML-escaped by hand below, since render_template()'s Jinja
				# env isn't autoescaping (confirmed against
				# frappe.utils.jinja.get_jenv()) and every value here comes
				# from an unauthenticated public form; escape first, *then*
				# turn our own newline substitution into real <br> tags, so
				# only the tags we add stay unescaped.
				message=frappe.render_template(  # nosemgrep: frappe-ssti
					"""
					<p><b>Name:</b> {{ doc.full_name }}</p>
					<p><b>Email:</b> {{ doc.email }}</p>
					<p><b>Phone:</b> {{ doc.phone or "-" }}</p>
					<p><b>Message:</b></p>
					<p>{{ doc.message }}</p>
					""",
					{
						"doc": {
							"full_name": escape_html(self.full_name),
							"email": escape_html(self.email or ""),
							"phone": escape_html(self.phone) if self.phone else None,
							"message": escape_html(self.message or "").replace("\n", "<br>"),
						}
					},
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
