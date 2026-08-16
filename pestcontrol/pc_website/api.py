# Copyright (c) 2026, QP and contributors
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
	full_name: str, email: str, phone: str, position_applied_for: str = "", message: str = ""
):
	"""Create a Job Application from the public careers form, attaching the
	resume file (if provided) as a private File once the doc's name exists."""
	doc = frappe.get_doc(
		{
			"doctype": "Job Application",
			"full_name": full_name,
			"email": email,
			"phone": phone,
			"position_applied_for": position_applied_for,
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
