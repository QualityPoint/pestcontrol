import frappe
from pestcontrol.custom.custom_fields import (
    make_custom_fields,
    delete_custom_fields
)
# from pestcontrol.custom.property_setter import (
#     create_property_setter,
#     remove_property_setter
# )
from pestcontrol.custom.fixtures import make_fixtures


def after_install():
    # create_property_setter()
    make_custom_fields()
    make_fixtures()
    # set_single_defaults()


def before_uninstall():
    # remove_property_setter()
    delete_custom_fields()


def set_single_defaults():
    """Set default values for single DocTypes"""
    for dt in (
        "WMS Settings"
    ):
        default_values = frappe.db.sql(
            """select fieldname, `default` from `tabDocField`
            where parent=%s""",
            dt,
        )
        if default_values:
            try:
                doc = frappe.get_doc(dt, dt)
                for fieldname, value in default_values:
                    doc.set(fieldname, value)
                doc.flags.ignore_mandatory = True
                doc.save()
            except frappe.ValidationError:
                pass
