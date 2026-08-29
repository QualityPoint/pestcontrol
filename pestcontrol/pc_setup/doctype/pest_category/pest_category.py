# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PestCategory(Document):
	pass


@frappe.whitelist()
def get_all_pest_types():
	"""Return all enabled pest types, used by the Pest Category editor grid."""
	return frappe.get_all(
		"Pest Type",
		filters={"disabled": 0},
		pluck="name",
		order_by="name",
	)


@frappe.whitelist()
def get_all_pest_categories():
	"""Return all pest categories, used by the facility-row category selector."""
	return frappe.get_all("Pest Category", pluck="name", order_by="name")


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def pest_type_by_category(doctype, txt, searchfield, start, page_len, filters):
	"""Link-query for a `pest_type` field that should only offer Pest Types
	belonging to a chosen Pest Category (e.g. Website Pest's pest_type field).

	`filters` arrives JSON-stringified from the Link field's set_query, same as
	pest_control_settings.get_uoms_by_category.
	"""
	if isinstance(filters, str):
		filters = frappe.parse_json(filters) if filters else {}
	category = (filters or {}).get("category")
	if not category:
		return []
	names = [p.pest_type for p in frappe.get_cached_doc("Pest Category", category).pests if p.pest_type]
	if not names:
		return []
	return frappe.get_all(
		"Pest Type",
		filters={"name": ["in", names], "disabled": 0, "pest_name": ["like", f"%{txt}%"]},
		fields=["name"],
		order_by="pest_name asc",
		start=start,
		page_length=page_len,
		as_list=True,
	)


@frappe.whitelist()
def get_pest_types_for_categories(categories: str | list):
	"""Return the union of pest types belonging to the given pest categories.

	`categories` may be a JSON list (from frappe.xcall) or a newline-joined
	string. Used to expand selected categories into pest types on a facility row.
	"""
	if isinstance(categories, str):
		categories = (
			frappe.parse_json(categories)
			if categories.strip().startswith("[")
			else [c.strip() for c in categories.splitlines() if c.strip()]
		)

	pests = set()
	for name in categories or []:
		category = frappe.get_cached_doc("Pest Category", name)
		pests.update(p.pest_type for p in category.pests)

	return sorted(pests)


def populate_pests_from_categories(
	doc,
	category_field="pest_category",
	pests_field="pests",
	category_link_field="pest_category",
	pest_link_field="pest_type",
):
	"""Expand the selected Pest Categories into the flat `pests` table.

	Mirror of User.populate_role_profile_roles: union the pest types of every
	selected category, drop pests no longer covered by any category, then append
	the new ones. No-op when no category is selected, leaving manual edits intact.
	Idempotent: safe to run on every save.
	"""
	categories = doc.get(category_field)
	if not categories:
		return

	new_pests = set()
	for row in categories:
		category = frappe.get_cached_doc("Pest Category", row.get(category_link_field))
		new_pests.update(p.get(pest_link_field) for p in category.pests)

	# keep only still-valid rows, then append the missing ones
	kept = [p for p in doc.get(pests_field) if p.get(pest_link_field) in new_pests]
	doc.set(pests_field, kept)
	existing = {p.get(pest_link_field) for p in kept}
	for pest_type in new_pests:
		if pest_type not in existing:
			doc.append(pests_field, {pest_link_field: pest_type})
