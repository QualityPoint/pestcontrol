# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

from pestcontrol.pc_website.utils import (
	attach_articles,
	get_website_context,
	make_route,
	route_from_article,
	validate_articles,
)


class WebsiteBlogPost(WebsiteGenerator):
	website = frappe._dict(template="pestcontrol/templates/generators/website_blog_post.html")

	def validate(self):
		validate_articles(self)

	def before_save(self):
		if not self.route:
			title = route_from_article(self)
			if title:
				self.route = f"blog/{make_route(title)}"

	def get_context(self, context):
		get_website_context(context)
		context.no_cache = 1
		attach_articles("Website Blog Post", [self])
