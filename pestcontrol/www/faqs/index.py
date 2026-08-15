from pestcontrol.pc_website.utils import get_translated_list, get_website_context


def get_context(context):
	get_website_context(context)
	context.no_cache = 1

	faqs = get_translated_list(
		"Website FAQ",
		filters={"published": 1},
		fields="*",
		order_by="faq_group asc, display_order asc",
	)

	groups = {}
	for faq in faqs:
		groups.setdefault(faq.faq_group or "General", []).append(faq)
	context.faq_groups = groups
