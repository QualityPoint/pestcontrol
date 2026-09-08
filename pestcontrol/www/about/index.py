import frappe
from frappe import _

from pestcontrol.pc_website.utils import get_language_row, get_translated_list, get_website_context


# Listed in /sitemap.xml. frappe's www sitemap only includes pages that
# opt in with this module attribute (website/router.py load_properties_from_controller).
sitemap = 1


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.title = _("About Us")
	context.description = _(
		"Learn about Skystar, our licensed pest control team, our eco-friendly methods and our commitment to protecting homes and businesses across Saudi Arabia."
	)
	context.page_h1 = _("About us")
	context.breadcrumbs = [
		{"label": _("home"), "route": ""},
		{"label": _("about us"), "route": "about"},
	]

	about_page = frappe.get_cached_doc("Website About Page").as_dict()
	context.about = get_language_row(about_page.get("content") or [])

	context.team_members = get_translated_list(
		"Website Team Member",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc",
		limit_page_length=4,
	)
	context.faqs = get_translated_list(
		"Website FAQ",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc",
		limit_page_length=5,
	)
	context.testimonials = get_translated_list(
		"Website Testimonial",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc",
		limit_page_length=4,
	)
