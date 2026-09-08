import frappe
from frappe import _

from pestcontrol.pc_website.utils import filter_by_language, get_translated_list, get_website_context


# Listed in /sitemap.xml. frappe's www sitemap only includes pages that
# opt in with this module attribute (website/router.py load_properties_from_controller).
sitemap = 1


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.title = _("Pricing")
	context.description = _(
		"Compare Skystar pest control plans and pricing. Transparent packages for homes, offices and commercial facilities."
	)
	context.page_h1 = _("Pricing plan")
	context.breadcrumbs = [
		{"label": _("home"), "route": ""},
		{"label": _("pricing"), "route": "pricing"},
	]
	context.plans = get_translated_list(
		"Website Pricing Plan",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc",
	)

	for plan in context.plans:
		rows = frappe.get_all(
			"Pricing Plan Feature",
			filters={"parent": plan.name},
			fields=["name", "is_included", "feature_text", "language"],
			order_by="idx asc",
		)
		plan.features = filter_by_language(rows)

	context.testimonials = get_translated_list(
		"Website Testimonial",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc",
		limit_page_length=4,
	)
