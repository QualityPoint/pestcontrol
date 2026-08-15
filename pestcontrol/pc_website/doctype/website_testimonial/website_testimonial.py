# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

from frappe.model.document import Document

from pestcontrol.pc_website.utils import validate_articles


class WebsiteTestimonial(Document):
	def validate(self):
		validate_articles(self)
