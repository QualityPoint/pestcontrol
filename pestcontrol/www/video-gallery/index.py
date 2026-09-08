from frappe import _

from pestcontrol.pc_website.utils import get_translated_list, get_website_context


# Listed in /sitemap.xml. frappe's www sitemap only includes pages that
# opt in with this module attribute (website/router.py load_properties_from_controller).
sitemap = 1


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.title = _("Video Gallery")
	context.description = _(
		"Videos showing Skystar's pest control methods, equipment and treatment process."
	)
	context.page_h1 = _("Our videos")
	context.breadcrumbs = [
		{"label": _("home"), "route": ""},
		{"label": _("videos"), "route": "video-gallery"},
	]
	context.gallery_items = get_translated_list(
		"Website Gallery Item",
		filters={"published": 1, "media_type": "Video"},
		fields="*",
		order_by="display_order asc",
	)
