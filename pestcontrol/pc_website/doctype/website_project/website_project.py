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


class WebsiteProject(WebsiteGenerator):
	website = frappe._dict(
		template="pestcontrol/templates/generators/website_project.html",
		page_title_field="page_title",
		condition_field="published",
	)

	def validate(self):
		validate_articles(self)
		apply_generator_route(self, "project")
		super().validate()

	def get_context(self, context):
		get_website_context(context)
		context.no_cache = 1
		attach_articles("Website Project", [self])
		context.page_h1 = localize(self, "project_name")
		context.page_header_image = self.header_image
		context.breadcrumbs = [
			{"label": _("home"), "route": ""},
			{"label": _("projects"), "route": "projects"},
			{"label": context.page_h1, "route": self.route},
		]
