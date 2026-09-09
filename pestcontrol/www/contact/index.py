from frappe import _

from pestcontrol.pc_website.utils import get_website_context

# Listed in /sitemap.xml. frappe's www sitemap only includes pages that
# opt in with this module attribute (website/router.py load_properties_from_controller).
sitemap = 1


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.title = _("Contact Us")
	context.description = _(
		"Get in touch with Skystar for a pest control quote, a site survey or emergency treatment. Phone, WhatsApp and branch details."
	)
	context.page_h1 = _("Contact us")
	context.breadcrumbs = [
		{"label": _("home"), "route": ""},
		{"label": _("contact us"), "route": "contact"},
	]
