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


class WebsitePest(WebsiteGenerator):
	website = frappe._dict(template="pestcontrol/templates/generators/website_pest.html")

	def validate(self):
		validate_articles(self)
		self.validate_pest_type_in_category()

	def validate_pest_type_in_category(self):
		"""The pest_type field is UI-filtered to the selected category's members
		(see website_pest.js); enforce the same rule server-side so a bypassed
		client can't persist a mismatch."""
		if not (self.pest_type and self.category):
			return
		allowed = {p.pest_type for p in frappe.get_cached_doc("Pest Category", self.category).pests}
		if self.pest_type not in allowed:
			frappe.throw(
				frappe._("Pest Type {0} does not belong to category {1}").format(
					frappe.bold(self.pest_type), frappe.bold(self.category)
				)
			)

	def before_save(self):
		if not self.route:
			title = route_from_article(self)
			if title:
				self.route = f"pest-library/{make_route(title)}"

	def get_context(self, context):
		get_website_context(context)
		context.no_cache = 1
		attach_articles("Website Pest", [self])
