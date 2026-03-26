import frappe
from frappe import _

from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def custom_fields():
    """Waqf specific custom fields that need to be added to the masters in ERPNext"""
    return {
        "Address": [
            {
                "fieldname": "location_tab",
                "fieldtype": "Tab Break",
                "label": _("Location"),
                "insert_after": "links",
            }
        ]
    }


def make_custom_fields():
    """Create WMS specific custom fields"""
    create_custom_fields(custom_fields(), ignore_validate=True)


def delete_custom_fields():
    """
    :param custom_fields: a dict like `{'Company': [{fieldname: 'crn', ...}]}`
    """
    for doctype, fields in custom_fields().items():
        frappe.db.delete(
            "Custom Field",
            {
                "fieldname": ("in", [field["fieldname"] for field in fields]),
                "dt": doctype,
            },
        )

        frappe.clear_cache(doctype=doctype)
