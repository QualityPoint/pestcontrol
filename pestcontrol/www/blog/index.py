from frappe import _

from pestcontrol.pc_website.utils import css_class_for, get_translated_list, get_website_context


# Listed in /sitemap.xml. frappe's www sitemap only includes pages that
# opt in with this module attribute (website/router.py load_properties_from_controller).
sitemap = 1


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	context.title = _("Blog")
	context.description = _(
		"Practical pest control advice, prevention tips and seasonal guidance from the Skystar team."
	)
	context.page_h1 = _("Our blog")
	context.breadcrumbs = [
		{"label": _("home"), "route": ""},
		{"label": _("blog"), "route": "blog"},
	]
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
	context.category_class = css_class_for
