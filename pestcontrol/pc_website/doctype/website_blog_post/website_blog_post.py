# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

from pestcontrol.pc_website.utils import (
	apply_generator_route,
	attach_articles,
	get_website_context,
	validate_articles,
)


class WebsiteBlogPost(WebsiteGenerator):
	website = frappe._dict(
		template="pestcontrol/templates/generators/website_blog_post.html",
		page_title_field="page_title",
		condition_field="published",
	)

	def validate(self):
		validate_articles(self)
		apply_generator_route(self, "blog")
		super().validate()

	def get_context(self, context):
		get_website_context(context)
		context.no_cache = 1
		attach_articles("Website Blog Post", [self])
