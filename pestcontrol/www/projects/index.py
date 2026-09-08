from frappe import _

from pestcontrol.pc_website.utils import css_class_for, get_translated_list, get_website_context


# Listed in /sitemap.xml. frappe's www sitemap only includes pages that
# opt in with this module attribute (website/router.py load_properties_from_controller).
sitemap = 1


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.title = _("Projects")
	context.description = _(
		"Browse completed Skystar pest control projects across residential, commercial and industrial sites in Saudi Arabia."
	)
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
	context.category_class = css_class_for
