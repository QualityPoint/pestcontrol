# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

from pestcontrol.pc_website.utils import attach_articles, get_website_context, make_route, validate_articles


class WebsiteTeamMember(WebsiteGenerator):
	website = frappe._dict(template="pestcontrol/templates/generators/website_team_member.html")

	def validate(self):
		validate_articles(self)

	def before_save(self):
		if not self.route:
			self.route = f"team/{make_route(self.member_name)}"

	def get_context(self, context):
		get_website_context(context)
		context.no_cache = 1
		attach_articles("Website Team Member", [self])
