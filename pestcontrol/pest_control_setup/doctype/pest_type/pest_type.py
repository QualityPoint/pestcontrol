# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils.nestedset import NestedSet


class PestType(NestedSet):
    def validate(self):
        self.set_one_root()
        self.validate_severity_level_rates()

    def set_one_root(self):
        if not self.parent_pest_type and not frappe.flags.in_test:
            if frappe.db.exists("Pest Type", _("All Pest Types")):
                self.parent_pest_type = _("All Pest Types")

    def validate_severity_level_rates(self):
        if self.apply_severity_rates:
            if not self.severity_level_rates or len(self.severity_level_rates) == 0:
                frappe.throw(_("Please add at least one Severity Level Rate."))

    def on_update(self):
        NestedSet.on_update(self)
        self.validate_one_root()
        self.delete_child_pest_types_key()

    def on_trash(self):
        NestedSet.on_trash(self, allow_root_deletion=True)
        self.delete_child_pest_types_key()

    def delete_child_pest_types_key(self):
        frappe.cache().hdel("child_pest_types", self.name)
