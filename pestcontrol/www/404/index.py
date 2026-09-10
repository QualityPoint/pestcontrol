from frappe import _

from pestcontrol.pc_website.utils import get_website_context


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.title = _("Page Not Found")
	# Nothing here should ever appear in search results.
	context.seo_noindex = True
	context.page_h1 = _("Page not found")
	context.breadcrumbs = [
		{"label": _("home"), "route": ""},
		{"label": _("404 error page"), "route": "404"},
	]
