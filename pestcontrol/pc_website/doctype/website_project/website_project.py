# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

from frappe.model.document import Document

from pestcontrol.pc_website.utils import make_route, route_from_article, validate_articles


class WebsiteProject(Document):
	def validate(self):
		validate_articles(self)

	def before_save(self):
		if not self.route:
			title = route_from_article(self)
			if title:
				self.route = make_route(title)
