# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

from frappe.model.document import Document

from pestcontrol.pc_website.utils import make_route, validate_articles


class WebsiteTeamMember(Document):
	def validate(self):
		validate_articles(self)

	def before_save(self):
		if not self.route:
			self.route = make_route(self.member_name)
