# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

from frappe.model.document import Document

from pestcontrol.pc_website.utils import validate_unique_language


class WebsiteAboutPage(Document):
	def validate(self):
		validate_unique_language(self, "content")
