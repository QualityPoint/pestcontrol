# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.website.website_generator import WebsiteGenerator

from pestcontrol.pc_website.utils import (
	apply_generator_route,
	attach_articles,
	get_website_context,
	localize,
	validate_articles,
)


class WebsiteService(WebsiteGenerator):
	website = frappe._dict(
		template="pestcontrol/templates/generators/website_service.html",
		page_title_field="page_title",
		condition_field="published",
	)

	def validate(self):
		validate_articles(self)
		apply_generator_route(self, "service")
		super().validate()

	def get_context(self, context):
		get_website_context(context)
		context.no_cache = 1
		attach_articles("Website Service", [self])
		context.page_h1 = localize(self, "service_name")
		context.page_header_image = self.header_image
		context.breadcrumbs = [
			{"label": _("home"), "route": ""},
			{"label": _("services"), "route": "services"},
			{"label": context.page_h1, "route": self.route},
		]
