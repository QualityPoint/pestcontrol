from frappe import _

from pestcontrol.pc_website.utils import get_translated_list, get_website_context, make_route


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.page_h1 = _("Our projects")
	context.breadcrumbs = [
		{"label": _("home"), "route": ""},
		{"label": _("project"), "route": "projects"},
	]
	context.projects = get_translated_list(
		"Website Project",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc",
	)
	context.categories = sorted(
		{p.category for p in context.projects if p.category},
		key=lambda c: c,
	)
	context.category_class = make_route
