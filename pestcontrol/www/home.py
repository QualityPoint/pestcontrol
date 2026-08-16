import frappe
from frappe import _

from pestcontrol.pc_website.utils import (
	filter_by_language,
	get_language_row,
	get_translated_list,
	get_website_context,
	localize,
	make_route,
)


def get_context(context):
	get_website_context(context)
	context.no_cache = 1

	about_page = frappe.get_cached_doc("Website About Page").as_dict()
	context.about = get_language_row(about_page.get("content") or [])

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

	for plan in context.plans:
		rows = frappe.get_all(
			"Pricing Plan Feature",
			filters={"parent": plan.name},
			fields=["name", "is_included", "feature_text", "language"],
			order_by="idx asc",
		)
		plan.features = filter_by_language(rows)

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

	context.best_services = get_translated_list(
		"Website Feature",
		filters={"section": "Best Services", "published": 1},
		fields="*",
		order_by="display_order asc",
	)
	context.features = get_translated_list(
		"Website Feature",
		filters={"section": "Features", "published": 1},
		fields="*",
		order_by="display_order asc",
	)
	context.why_choose_us = get_translated_list(
		"Website Feature",
		filters={"section": "Why Choose Us", "published": 1},
		fields="*",
		order_by="display_order asc",
	)
	context.about_list = get_translated_list(
		"Website List Item",
		filters={"list_key": "About List", "published": 1},
		fields="*",
		order_by="display_order asc",
	)
	context.pricing_benefits = get_translated_list(
		"Website List Item",
		filters={"list_key": "Pricing Benefits", "published": 1},
		fields="*",
		order_by="display_order asc",
	)
	context.cta_benefits = get_translated_list(
		"Website List Item",
		filters={"list_key": "CTA Benefits", "published": 1},
		fields="*",
		order_by="display_order asc",
	)

	# Fixed fallback labels used position-by-position until an admin seeds
	# real "Counter Labels" rows — keeps the 4 slots aligned with PC Website
	# Settings' fixed years/projects/team/satisfaction field order.
	counter_label_defaults = [
		_("Years Of Experience"),
		_("Projects Completed"),
		_("Dedicated Team"),
		_("Happy Customers"),
	]
	counter_label_rows = get_translated_list(
		"Website List Item",
		filters={"list_key": "Counter Labels", "published": 1},
		fields="*",
		order_by="display_order asc",
	)
	context.counter_labels = [
		localize(counter_label_rows[i], "title") if i < len(counter_label_rows) else counter_label_defaults[i]
		for i in range(4)
	]
