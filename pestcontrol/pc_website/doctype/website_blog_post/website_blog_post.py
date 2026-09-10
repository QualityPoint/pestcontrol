# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

from pestcontrol.pc_website.utils import (
	attach_articles,
	get_website_context,
	localize,
	route_from_article,
	validate_articles,
)


class WebsiteBlogPost(WebsiteGenerator):
	website = frappe._dict(template="pestcontrol/templates/generators/website_blog_post.html")

	def validate(self):
		validate_articles(self)
		if not self.route:
			# self.scrub() is frappe's cleanup_page_name: Unicode-safe, so a
			# non-Latin title slugs to itself instead of to an empty string.
			if title := route_from_article(self):
				self.route = f"blog/{self.scrub(title)}"
		super().validate()

	def get_context(self, context):
		get_website_context(context)
		context.no_cache = 1
		attach_articles("Website Blog Post", [self])
		# Per-language title from the article bundle. Without it frappe falls
		# back to get_title_field() -> "name", which is a hash for this
		# autoname:hash doctype, and the page title becomes the hash.
		context.title = localize(self, "title")

	def before_save(self):
		# set the title field from the first row title field in content child table
		if self.article and self.article[0].title:
			self.title = self.article[0].title

	def genrateRoute(self):
		# I wanna generate the route from the first row title field in content child table and Take into consideration language and localization
		if self.article and self.article[0].title:
			title = self.article[0].title
			# Generate the route based on the title and language
			self.route = f"blog/{self.scrub(title)}"
