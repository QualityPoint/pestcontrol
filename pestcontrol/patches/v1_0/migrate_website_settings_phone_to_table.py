# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

"""`PC Website Settings.phone` (Data) became `phone_numbers` (child table of
Website Phone Number). Carry the single existing value across as one primary row.

Idempotent: skips if there is nothing to migrate or rows already exist.
"""

import frappe


def execute():
	# Read straight from `tabSingles` — `get_single_value` now validates the
	# fieldname against the (already updated) meta and would raise, since
	# `phone` no longer exists on the doctype; `get_value` on "Singles" adds an
	# `ORDER BY creation` the table doesn't have. Raw SQL avoids both.
	row = frappe.db.sql(
		"select value from tabSingles where doctype = %s and field = %s",
		("PC Website Settings", "phone"),
	)
	old = row[0][0] if row else None
	if not old:
		return

	settings = frappe.get_single("PC Website Settings")
	if settings.get("phone_numbers"):
		return

	settings.append("phone_numbers", {"phone_number": old, "is_primary": 1})
	settings.save(ignore_permissions=True)
