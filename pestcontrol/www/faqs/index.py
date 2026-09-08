from frappe import _

from pestcontrol.pc_website.utils import get_translated_list, get_website_context


# Listed in /sitemap.xml. frappe's www sitemap only includes pages that
# opt in with this module attribute (website/router.py load_properties_from_controller).
sitemap = 1


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.title = _("FAQs")
	context.description = _(
		"Answers to the questions we are asked most about pest control treatments, safety, scheduling and what to expect from a visit."
	)
	context.page_h1 = _("Frequently asked question")
	context.breadcrumbs = [
		{"label": _("home"), "route": ""},
		{"label": _("FAQs"), "route": "faqs"},
	]

	faqs = get_translated_list(
		"Website FAQ",
		filters={"published": 1},
		fields="*",
		order_by="faq_group asc, display_order asc",
	)

	groups = {}
	for faq in faqs:
		groups.setdefault(faq.faq_group or "General", []).append(faq)
	context.faq_groups = groups
