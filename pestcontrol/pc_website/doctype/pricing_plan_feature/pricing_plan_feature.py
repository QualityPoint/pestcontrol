# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

from frappe.model.document import Document

from pestcontrol.pc_website.utils import validate_translations


class PricingPlanFeature(Document):
	def validate(self):
		validate_translations(self)
