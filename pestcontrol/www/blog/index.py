from pestcontrol.pc_website.utils import get_translated_list, get_website_context, make_route


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.blog_posts = get_translated_list(
		"Website Blog Post",
		filters={"published": 1},
		fields="*",
		order_by="published_on desc, creation desc",
	)
	context.categories = sorted(
		{p.blog_category for p in context.blog_posts if p.blog_category},
		key=lambda c: c,
	)
	context.category_class = make_route
