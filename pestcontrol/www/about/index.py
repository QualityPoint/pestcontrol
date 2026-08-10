import frappe

from pestcontrol.pc_website.utils import get_language_row, get_translated_list, get_website_context


def get_context(context):
	get_website_context(context)
	context.no_cache = 1

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
