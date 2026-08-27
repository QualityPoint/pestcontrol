# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.file_manager import save_file


# Reviewed: intentionally public, this is the site's own contact form
# endpoint; no permission check applies since anonymous visitors are
# exactly who's meant to call it.
@frappe.whitelist(allow_guest=True)  # nosemgrep: guest-whitelisted-method
def submit_contact_form(fname: str, lname: str = "", email: str = "", phone: str = "", message: str = ""):
	"""Create a Website Contact Message from the public contact form."""
	full_name = f"{fname} {lname}".strip()
	doc = frappe.get_doc(
		{
			"doctype": "Website Contact Message",
			"full_name": full_name,
			"email": email,
			"phone": phone,
			"message": message,
			"status": "New",
		}
	)
	doc.insert(ignore_permissions=True)
	return {"success": True}


# Reviewed: intentionally public, this is the site's own job application
# form endpoint; no permission check applies since anonymous applicants are
# exactly who's meant to call it.
@frappe.whitelist(allow_guest=True)  # nosemgrep: guest-whitelisted-method
def submit_job_application(
	full_name: str,
	email: str,
	phone: str,
	position_applied_for: str = "",
	job_opening: str = "",
	message: str = "",
):
	"""Create a Job Application from the public careers form, attaching the
	resume file (if provided) as a private File once the doc's name exists.

	The careers form's position selector is populated from HRMS Job Openings, so
	it POSTs a `job_opening` id. When that id resolves to a real opening we link
	it and snapshot its title into `position_applied_for` (never trusting a
	client-sent title); otherwise we fall back to the free-text value, which is
	also what the form sends when there are no open positions to list."""
	title = position_applied_for
	linked_opening = None
	if job_opening:
		row = frappe.db.get_value("Job Opening", job_opening, ["name", "job_title"], as_dict=True)
		if row:
			linked_opening = row.name
			title = row.job_title

	doc = frappe.get_doc(
		{
			"doctype": "Job Application",
			"full_name": full_name,
			"email": email,
			"phone": phone,
			"position_applied_for": title,
			"job_opening": linked_opening,
			"message": message,
			"status": "New",
		}
	)
	doc.insert(ignore_permissions=True)

	resume_file = frappe.request.files.get("resume") if frappe.request else None
	if resume_file and resume_file.filename:
		file_doc = save_file(
			resume_file.filename,
			resume_file.read(),
			"Job Application",
			doc.name,
			is_private=1,
			df="resume",
		)
		doc.db_set("resume", file_doc.file_url, update_modified=False)

	doc.notify_admin()
	return {"success": True}


@frappe.whitelist()
def get_portal_document(doctype: str, name: str):
	"""Read-only JSON pass-through for the customer dashboard's detail view.

	Re-exposes the same check erpnext.templates.pages.order.py already uses
	to gate /orders/<name> etc. — grants nothing new, just makes that
	existing permission decision reachable as JSON instead of a Jinja page.
	"""
	doc = frappe.get_doc(doctype, name)
	if not frappe.has_website_permission(doc):
		frappe.throw(frappe._("Not Permitted"), frappe.PermissionError)
	return doc.as_dict()
