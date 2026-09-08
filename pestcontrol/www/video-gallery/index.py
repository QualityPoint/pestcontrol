from frappe import _

from pestcontrol.pc_website.utils import get_translated_list, get_website_context


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
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
