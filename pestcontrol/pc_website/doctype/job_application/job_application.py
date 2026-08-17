# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import escape_html


class JobApplication(Document):
	def notify_admin(self):
		"""Send the new-application alert email. Called explicitly by the
		submit_job_application API endpoint once the resume (if any) has
		been attached — not wired as an after_insert hook, since the resume
		file is attached in a separate step *after* insert() completes (its
		File record needs this doc's generated `name` to attach to), so an
		after_insert hook would always report "no resume" even when one was
		uploaded."""
		notify_email = frappe.db.get_single_value("PC Website Settings", "email")
		if not notify_email:
			return

		# Queued (not `now=True`) so a broken/unconfigured mail server never
		# blocks or breaks the applicant's actual submission — capturing the
		# application always has to succeed regardless of whether the alert
		# does. Mirrors website_contact_message.py's after_insert exactly.
		try:
			frappe.sendmail(
				recipients=[notify_email],
				subject=f"New job application from {self.full_name}",
				# Reviewed: template string is a fixed literal, never derived
				# from user input, so this isn't template injection — only
				# field *values* are interpolated. Those values are still
				# HTML-escaped by hand below, since render_template()'s Jinja
				# env isn't autoescaping and every value here comes from an
				# unauthenticated public form.
				message=frappe.render_template(  # nosemgrep: frappe-ssti
					"""
					<p><b>Name:</b> {{ doc.full_name }}</p>
					<p><b>Email:</b> {{ doc.email }}</p>
					<p><b>Phone:</b> {{ doc.phone }}</p>
					<p><b>Position:</b> {{ doc.position_applied_for or "-" }}</p>
					<p><b>Message:</b></p>
					<p>{{ doc.message }}</p>
					<p><b>Resume:</b> {{ "Attached" if doc.has_resume else "Not attached" }}</p>
					""",
					{
						"doc": {
							"full_name": escape_html(self.full_name),
							"email": escape_html(self.email or ""),
							"phone": escape_html(self.phone or ""),
							"position_applied_for": escape_html(self.position_applied_for)
							if self.position_applied_for
							else None,
							"message": escape_html(self.message or "").replace("\n", "<br>"),
							"has_resume": bool(self.resume),
						}
					},
				),
				reference_doctype=self.doctype,
				reference_name=self.name,
			)
		except Exception:
			frappe.log_error(title="Failed to queue job application alert email")
			# frappe.throw()/msgprint() inside sendmail() already queued a
			# message (e.g. "no outgoing email account configured") before
			# raising — clear it so it doesn't leak into the guest's API
			# response; the form submission itself must look unaffected.
			frappe.clear_messages()
