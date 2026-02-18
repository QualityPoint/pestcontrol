# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class OperationVisit(Document):
    def validate(self):
        self.validate_visit_no()
        self.validate_supervisor()

    def validate_visit_no(self):
        if self.visit_no:
            existing_visit = frappe.db.get_value(
                "Operation Visit", {"visit_no": self.visit_no,
                                    "company": self.company,
                                    "name": ["!=", self.name]}, "name")
            if existing_visit:
                frappe.throw(
                    _("Visit No {0} already exists for another Operation Visit.").format(self.visit_no))

    def validate_supervisor(self):
        if not frappe.db.get_value("Operation Team Member", self.operation_supervisor, "is_supervisor"):
            frappe.throw(
                _("{0} is not a valid supervisor.").format(self.operation_supervisor))
