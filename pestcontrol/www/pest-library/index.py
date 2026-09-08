from frappe import _

from pestcontrol.pc_website.utils import get_translated_list, get_website_context, make_route


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
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
	context.category_class = make_route
