from frappe import _

from pestcontrol.pc_website.utils import get_translated_list, get_website_context


# Listed in /sitemap.xml. frappe's www sitemap only includes pages that
# opt in with this module attribute (website/router.py load_properties_from_controller).
sitemap = 1


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.title = _("Our Team")
	context.description = _(
		"Meet the licensed technicians and specialists behind Skystar's pest control and environmental services."
	)
	context.page_h1 = _("Our team")
	context.breadcrumbs = [
		{"label": _("home"), "route": ""},
		{"label": _("our team"), "route": "team"},
	]
	context.team_members = get_translated_list(
		"Website Team Member",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc",
	)
