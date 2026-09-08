from frappe import _

from pestcontrol.pc_website.utils import get_website_context


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.page_h1 = _("Contact us")
	context.breadcrumbs = [
		{"label": _("home"), "route": ""},
		{"label": _("contact us"), "route": "contact"},
	]
