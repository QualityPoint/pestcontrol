# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils.nestedset import NestedSet


class AddressDivisionType(NestedSet):
    nsm_parent_field = "parent_division_type"

    def validate(self):
        self.validate_parent_division()

    def validate_parent_division(self):
        if self.parent_division_type:
            parent_division = frappe.get_doc(
                "Address Division Type", self.parent_division_type)
            if parent_division.is_group == 0:
                frappe.throw(_("Parent Division Type must be a group"))

            if parent_division.country != self.country:
                frappe.throw(
                    _("Parent Division Type must belong to the same country"))

    def update_nsm_model(self):
        frappe.utils.nestedset.update_nsm(self)

    def on_update(self):
        self.update_nsm_model()
        self.validate_one_root()

    def on_trash(self):
        self.update_nsm_model()


@frappe.whitelist()
def add_node():
    args = frappe.form_dict
    parent = args.get("parent") or args.get("parent_division_type") or ""
    # Don't set parent when it equals the doctype name (root level)
    if parent == "Address Division Type":
        parent = ""
    doc = frappe.get_doc({
        "doctype": "Address Division Type",
        "division_type": args.get("division_type") or args.get("name"),
        "parent_division_type": parent,
        "is_group": frappe.utils.cint(args.get("is_group", 0)),
        "country": args.get("country"),
    })
    doc.save()
    return doc.name


@frappe.whitelist()
def get_children(doctype, parent=None, country=None, is_root=False, is_tree=False):
    filters = []
    if country and country != "All Countries":
        filters.append(["country", "=", country])

    fields = ["name as value", "division_type as title", "is_group"]

    if is_root:
        parent = ""
    if parent and country and parent != country:
        filters.append(["parent_division_type", "=", parent])
    else:
        filters.append(["parent_division_type", "=", ""])

    members = frappe.get_list(
        doctype, fields=fields, filters=filters, order_by="name")

    for member in members:
        member.expandable = 1 if member.get("is_group") else 0

    return members
