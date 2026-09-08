# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.website.website_generator import WebsiteGenerator

from pestcontrol.pc_website.utils import (
	attach_articles,
	get_website_context,
	localize,
	route_from_article,
	validate_articles,
)


class WebsiteService(WebsiteGenerator):
	website = frappe._dict(template="pestcontrol/templates/generators/website_service.html")

	def validate(self):
		validate_articles(self)
		if not self.route:
			# self.scrub() is frappe's cleanup_page_name: Unicode-safe, so a
			# non-Latin title slugs to itself instead of to an empty string.
			if title := route_from_article(self):
				self.route = f"service/{self.scrub(title)}"
		super().validate()

	def get_context(self, context):
		get_website_context(context)
		context.no_cache = 1
		attach_articles("Website Service", [self])
		context.title = localize(self, "service_name")
		context.page_h1 = context.title
		context.page_header_image = self.header_image
		context.breadcrumbs = [
			{"label": _("home"), "route": ""},
			{"label": _("services"), "route": "services"},
			{"label": context.page_h1, "route": self.route},
		]
