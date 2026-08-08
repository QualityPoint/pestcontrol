import frappe

from pestcontrol.pc_website.utils import (
	attach_translations,
	get_translated_list,
	get_website_context,
	make_route,
)


def get_context(context):
	get_website_context(context)
	context.no_cache = 1

	context.services = get_translated_list(
		"Website Service",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc",
		limit_page_length=6,
	)
	context.projects = get_translated_list(
		"Website Project",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc",
		limit_page_length=6,
	)
	context.project_categories = sorted(
		{p.category for p in context.projects if p.category},
		key=lambda c: c,
	)
	context.category_class = make_route
	context.plans = get_translated_list(
		"Website Pricing Plan",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc",
	)

	all_features = []
	for plan in context.plans:
		plan.features = frappe.get_all(
			"Pricing Plan Feature",
			filters={"parent": plan.name},
			fields=["name", "feature_text", "is_included"],
			order_by="idx asc",
		)
		all_features.extend(plan.features)
	attach_translations("Pricing Plan Feature", all_features)

	context.faqs = get_translated_list(
		"Website FAQ",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc",
		limit_page_length=5,
	)
	context.testimonials = get_translated_list(
		"Website Testimonial",
		filters={"published": 1},
		fields="*",
		order_by="display_order asc",
		limit_page_length=4,
	)
	context.blog_posts = get_translated_list(
		"Website Blog Post",
		filters={"published": 1},
		fields="*",
		order_by="published_on desc, creation desc",
		limit_page_length=3,
	)
