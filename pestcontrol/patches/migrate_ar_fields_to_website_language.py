# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import frappe

# doctype -> {old "_ar" fieldname: matching default-language fieldname}
DOCTYPE_AR_FIELDS = {
	"PC Website Settings": {
		"address_ar": "address",
		"about_footer_text_ar": "about_footer_text",
	},
	"Pricing Plan Feature": {
		"feature_text_ar": "feature_text",
	},
	"Website Blog Post": {
		"title_ar": "title",
		"blog_intro_ar": "blog_intro",
		"content_ar": "content",
	},
	"Website FAQ": {
		"question_ar": "question",
		"answer_ar": "answer",
	},
	"Website Gallery Item": {
		"title_ar": "title",
	},
	"Website Pricing Plan": {
		"plan_name_ar": "plan_name",
	},
	"Website Project": {
		"project_name_ar": "project_name",
		"short_description_ar": "short_description",
		"full_description_ar": "full_description",
	},
	"Website Service": {
		"service_name_ar": "service_name",
		"short_description_ar": "short_description",
		"full_description_ar": "full_description",
	},
	"Website Team Member": {
		"designation_ar": "designation",
		"bio_ar": "bio",
	},
	"Website Testimonial": {
		"designation_ar": "designation",
		"testimonial_text_ar": "testimonial_text",
	},
}


def execute():
	"""Runs pre_model_sync, while the old `_ar` columns still exist on the
	parent tables. Copies any Arabic values into `Website-Language` rows
	before the schema sync (later in the same `bench migrate`) drops them."""
	# The child doctype itself doesn't exist yet on a site upgrading from the
	# old `_ar`-field schema — force-sync just this one doctype so we have a
	# table to write into. The parent doctypes are left untouched here; the
	# normal schema sync that follows this patch drops their `_ar` columns
	# and adds the `translations` field as usual.
	frappe.reload_doc("pc_website", "doctype", "website_language", force=True)

	for doctype, ar_field_map in DOCTYPE_AR_FIELDS.items():
		if not frappe.db.table_exists(doctype):
			continue

		existing_columns = set(frappe.db.get_table_columns(doctype))
		ar_fields = [f for f in ar_field_map if f in existing_columns]
		if not ar_fields:
			continue

		rows = frappe.db.get_all(doctype, fields=["name", *ar_fields])
		for row in rows:
			for ar_field in ar_fields:
				value = row.get(ar_field)
				if not value:
					continue
				frappe.get_doc(
					{
						"doctype": "Website-Language",
						"parenttype": doctype,
						"parent": row.name,
						"parentfield": "translations",
						"language": "ar",
						"fieldname": ar_field_map[ar_field],
						"translated_value": value,
					}
				).insert(ignore_permissions=True)

	frappe.db.commit()
