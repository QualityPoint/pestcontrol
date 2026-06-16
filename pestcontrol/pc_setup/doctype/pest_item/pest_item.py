# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PestItem(Document):
	def before_insert(self):
		if frappe.db.exists("Pest Item", {"parent": self.parent, "pest_type": self.pest_type}):
			frappe.throw(
				frappe._("Pest Category '{0}' already has the pest type '{1}'").format(
					self.parent, self.pest_type
				)
			)
