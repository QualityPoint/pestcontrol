# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils.nestedset import NestedSet


class AddressDivision(NestedSet):
    nsm_parent_field = "parent_division"

    def validate(self):
        self.validate_parent_division()

    def validate_parent_division(self):
        if self.division_type:
            division_type_doc = frappe.get_doc(
                "Address Division Type", self.division_type)

            if division_type_doc.parent_division_type and not self.parent_division:
                frappe.throw(
                    _("Parent Division is required because Division Type '{0}' is a child of '{1}'").format(
                        self.division_type, division_type_doc.parent_division_type
                    )
                )

            if not division_type_doc.parent_division_type and self.parent_division:
                self.parent_division = None

        if self.parent_division:
            parent = frappe.get_doc("Address Division", self.parent_division)

            if parent.is_group == 0:
                frappe.throw(_("Parent Division must be a group"))

            if parent.country != self.country:
                frappe.throw(
                    _("Parent Division must belong to the same country"))

            if self.division_type:
                expected_parent_type = frappe.db.get_value(
                    "Address Division Type", self.division_type, "parent_division_type")
                if expected_parent_type and parent.division_type != expected_parent_type:
                    frappe.throw(
                        _("Parent Division must be of Division Type '{0}', but '{1}' has Division Type '{2}'").format(
                            expected_parent_type,
                            self.parent_division,
                            parent.division_type or _("none")
                        )
                    )

    def update_nsm_model(self):
        frappe.utils.nestedset.update_nsm(self)

    def on_update(self):
        self.update_nsm_model()
        self.validate_one_root()

    def on_trash(self):
        self.update_nsm_model()


@frappe.whitelist()
def get_parent_division_type(division_type):
    return frappe.db.get_value("Address Division Type", division_type, "parent_division_type")


@frappe.whitelist()
def get_child_node_info(parent):
    """Return data needed to build the Add Child dialog for a given parent node."""
    parent_doc = frappe.db.get_value(
        "Address Division", parent, ["division_type", "country"], as_dict=True
    )
    if not parent_doc:
        frappe.throw(_("Parent Division '{0}' not found").format(parent))

    child_types = frappe.get_all(
        "Address Division Type",
        filters={"parent_division_type": parent_doc.division_type},
        pluck="name",
    )

    return {
        "country": parent_doc.country,
        "child_division_types": child_types,
    }


@frappe.whitelist()
def add_node():
    args = frappe.form_dict
    parent = args.get("parent") or ""
    if parent == "Address Division":
        parent = ""

    division_type = args.get("division_type")
    is_group = 1 if (
        division_type and frappe.db.exists(
            "Address Division Type", {"parent_division_type": division_type}
        )
    ) else 0

    doc = frappe.get_doc({
        "doctype": "Address Division",
        "division_name": args.get("division_name"),
        "parent_division": parent,
        "division_type": division_type,
        "country": args.get("country"),
        "is_group": is_group,
    })
    doc.save()
    return doc.name


@frappe.whitelist()
def get_children(doctype, parent=None, country=None, division_type=None, is_root=False, is_tree=False):
    filters = []
    if country and country != "All Countries":
        filters.append(["country", "=", country])
    if division_type:
        filters.append(["division_type", "=", division_type])

    fields = ["name as value", "division_name as title",
              "is_group", "division_type"]

    if is_root:
        parent = ""
    if parent and parent != "Address Division":
        filters.append(["parent_division", "=", parent])
    else:
        filters.append(["parent_division", "=", ""])

    members = frappe.get_list(
        doctype, fields=fields, filters=filters, order_by="name")

    for member in members:
        member.expandable = 1 if member.get("is_group") else 0

    return members
