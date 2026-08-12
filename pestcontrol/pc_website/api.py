# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import frappe


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
