from frappe import _

from pestcontrol.pc_website.utils import get_website_context


# Listed in /sitemap.xml. frappe's www sitemap only includes pages that
# opt in with this module attribute (website/router.py load_properties_from_controller).
sitemap = 1


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.title = _("Our Branches")
	context.description = _(
		"Find your nearest Skystar branch. Addresses, phone numbers and service areas across Saudi Arabia."
	)
	context.page_h1 = _("Our Branches")
	context.breadcrumbs = [
		{"label": _("home"), "route": ""},
		{"label": _("branches"), "route": "branches"},
	]
