from frappe import _

from pestcontrol.pc_website.utils import get_translated_list, get_website_context


# Listed in /sitemap.xml. frappe's www sitemap only includes pages that
# opt in with this module attribute (website/router.py load_properties_from_controller).
sitemap = 1


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.title = _("Services")
	context.description = _(
		"Explore Skystar's full range of pest control and environmental services, from termite and rodent treatment to commercial contracts and preventive programmes."
	)
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
