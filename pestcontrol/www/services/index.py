from frappe import _

from pestcontrol.pc_website.utils import get_translated_list, get_website_context


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.page_h1 = _("Our services")
	context.breadcrumbs = [
		{"label": _("home"), "route": ""},
		{"label": _("services"), "route": "services"},
	]
	context.services = get_translated_list(
		"Website Service",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc",
	)
	context.testimonials = get_translated_list(
		"Website Testimonial",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc",
		limit_page_length=4,
	)
