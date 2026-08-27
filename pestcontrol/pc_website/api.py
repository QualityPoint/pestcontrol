# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

import frappe
from frappe import _
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
	"""Create an HRMS Job Applicant from the public careers form, attaching the
	resume file (if provided) as a private File once the applicant's name exists.

	The careers form's position selector is populated from HRMS Job Openings, so
	it POSTs a `job_opening` id. We link it only if it is still Open — the
	dropdown only lists Open+published openings, but a race could send a
	just-closed one, and Job Applicant.before_insert throws hard on a closed
	opening. When no opening is linked (e.g. the free-text fallback shown when
	there are no open positions), the typed position is preserved in the cover
	letter instead."""
	linked_opening = None
	if job_opening:
		row = frappe.db.get_value("Job Opening", job_opening, ["name", "status"], as_dict=True)
		if row and row.status == "Open":
			linked_opening = row.name

	cover_letter = message or ""
	if not linked_opening and position_applied_for:
		cover_letter = f"{_('Position applied for')}: {position_applied_for}\n\n{cover_letter}".strip()

	doc = frappe.get_doc(
		{
			"doctype": "Job Applicant",
			"applicant_name": full_name,
			"email_id": email,
			"phone_number": phone,
			# Link -> Job Opening; `designation` auto-fetches from it
			"job_title": linked_opening,
			"status": "Open",
			"source": "Website Listing",
			"cover_letter": cover_letter or None,
		}
	)
	doc.insert(ignore_permissions=True)

	resume_file = frappe.request.files.get("resume") if frappe.request else None
	if resume_file and resume_file.filename:
		file_doc = save_file(
			resume_file.filename,
			resume_file.read(),
			"Job Applicant",
			doc.name,
			is_private=1,
			df="resume_attachment",
		)
		doc.db_set("resume_attachment", file_doc.file_url, update_modified=False)

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
