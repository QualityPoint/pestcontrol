# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import frappe


@frappe.whitelist(allow_guest=True)
def submit_contact_form(fname, lname="", email="", phone="", message=""):
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
	frappe.db.commit()
	return {"success": True}
