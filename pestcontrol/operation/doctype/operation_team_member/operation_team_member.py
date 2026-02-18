# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils.nestedset import NestedSet


class OperationTeamMember(NestedSet):
    nsm_parent_field = "parent_member"

    def before_validate(self):
        self.member_name = frappe.get_value(
            "Employee", self.team_member, "employee_name")

    def validate(self):
        self.validate_parent_member()

    def validate_parent_member(self):
        if self.parent_member == self.name:
            frappe.throw(
                _("{0} cannot report to himself.").format(self.member_name))

        if self.parent_member:
            if not frappe.db.get_value("Operation Team Member", self.parent_member, "is_supervisor"):
                frappe.throw(
                    _("{0} cannot report to {1} because {1} is not a supervisor.").format(self.member_name, self.parent_member))

    def update_nsm_model(self):
        frappe.utils.nestedset.update_nsm(self)

    def on_update(self):
        self.update_nsm_model()
        self.validate_one_root()

    def on_trash(self):
        self.update_nsm_model()


@frappe.whitelist()
def get_children(doctype, parent=None, company=None, is_root=False, is_tree=False):
    filters = []
    if company and company != "All Companies":
        filters.append(["company", "=", company])

    fields = ["name as value", "member_name as title"]

    if is_root:
        parent = ""
    if parent and company and parent != company:
        filters.append(["parent_member", "=", parent])
    else:
        filters.append(["parent_member", "=", ""])

    members = frappe.get_list(
        doctype, fields=fields, filters=filters, order_by="name")

    for member in members:
        is_expandable = frappe.get_all(
            doctype, filters=[["parent_member", "=", member.get("value")]])
        member.expandable = 1 if is_expandable else 0

    return members
