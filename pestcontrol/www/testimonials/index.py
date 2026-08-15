from pestcontrol.pc_website.utils import get_translated_list, get_website_context


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.testimonials = get_translated_list(
		"Website Testimonial",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc",
	)
