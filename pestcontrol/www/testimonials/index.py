from frappe import _

from pestcontrol.pc_website.utils import get_translated_list, get_website_context


# Listed in /sitemap.xml. frappe's www sitemap only includes pages that
# opt in with this module attribute (website/router.py load_properties_from_controller).
sitemap = 1


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.title = _("Testimonials")
	context.description = _(
		"Read what Skystar customers say about our pest control treatments, response times and technicians."
	)
	context.page_h1 = _("Testimonials")
	context.breadcrumbs = [
		{"label": _("home"), "route": ""},
		{"label": _("testimonials"), "route": "testimonials"},
	]
	context.testimonials = get_translated_list(
		"Website Testimonial",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc",
	)
