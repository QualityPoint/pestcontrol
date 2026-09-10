from frappe import _

from pestcontrol.pc_website.utils import css_class_for, get_translated_list, get_website_context

# Listed in /sitemap.xml. frappe's www sitemap only includes pages that
# opt in with this module attribute (website/router.py load_properties_from_controller).
sitemap = 1


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.title = _("Pest Library")
	context.description = _(
		"Identify common household and commercial pests, learn the risks they carry and see how Skystar treats each one."
	)
	context.page_h1 = _("Pest Library")
	context.breadcrumbs = [
		{"label": _("home"), "route": ""},
		{"label": _("pest library"), "route": "pest-library"},
	]
	context.pests = get_translated_list(
		"Website Pest",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc, creation desc",
	)
	context.categories = sorted(
		{p.category for p in context.pests if p.category},
		key=lambda c: c,
	)
	context.category_class = css_class_for
