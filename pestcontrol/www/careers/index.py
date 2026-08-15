from pestcontrol.pc_website.utils import get_website_context


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
