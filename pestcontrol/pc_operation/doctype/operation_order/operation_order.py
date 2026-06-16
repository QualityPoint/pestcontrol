# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from pestcontrol.pc_setup.doctype.pest_category.pest_category import (
	populate_pests_from_categories,
)


class OperationOrder(Document):
	def validate(self):
		self.populate_category_pests()

	@frappe.whitelist()
	def populate_category_pests(self):
		"""Expand the selected Pest Categories into the `pests` table."""
		populate_pests_from_categories(self)
