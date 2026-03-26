# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class VisitEntry(Document):
    def validate(self):
        self.validate_visit_no()
        self.validate_customer_project()
        self.validate_supervisor()
        self.validate_team_members()

    def validate_visit_no(self):
        if self.visit_no:
            existing_visit = frappe.db.get_value(
                "Operation Visit", {"visit_no": self.visit_no,
                                    "company": self.company,
                                    "name": ["!=", self.name]}, "name")
            if existing_visit:
                frappe.throw(
                    _("Visit No {0} already exists for another Operation Visit.").format(self.visit_no))

    def validate_customer_project(self):
        if self.customer and self.project:
            project_customer = frappe.db.get_value(
                "Project", self.project, "customer")
            if project_customer != self.customer:
                frappe.throw(
                    _("The selected Project does not belong to the selected Customer."))

    def validate_supervisor(self):
        if not frappe.db.get_value("Operation Team Member", self.operation_supervisor, "is_supervisor"):
            frappe.throw(
                _("{0} is not a valid supervisor.").format(self.operation_supervisor))

    def validate_team_members(self):
        """Ensure that all team members are related to the same company"""
        for team_member in self.team_members:
            member_company = frappe.db.get_value(
                "Operation Team Member", team_member.team_member, "company")
            if member_company != self.company:
                frappe.throw(
                    _("Team member {0} does not belong to the selected company {1}.").format(team_member.team_member, self.company))
