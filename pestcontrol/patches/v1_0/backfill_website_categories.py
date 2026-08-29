# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

"""Backfill category master records from the free-text / Select values that used
to live directly on Website Blog Post, Website Pest and Website Project, so the
existing rows stay valid now that `category` is a mandatory Link field.

Idempotent: only inserts a master record when it does not already exist.
"""

import frappe

# doctype -> (source fieldname, master doctype, master title fieldname)
MAP = {
	"Website Project": ("category", "Website Project Category", "title"),
	"Website Blog Post": ("blog_category", "Website Blog Category", "title"),
	"Website Pest": ("category", "Pest Category", "category_name"),
}


def execute():
	for doctype, (field, master, master_field) in MAP.items():
		if not frappe.db.table_exists(doctype):
			continue
		values = {
			(value or "").strip() for value in frappe.get_all(doctype, pluck=field) if (value or "").strip()
		}
		for title in sorted(values):
			if not frappe.db.exists(master, title):
				frappe.get_doc({"doctype": master, master_field: title}).insert(ignore_permissions=True)
