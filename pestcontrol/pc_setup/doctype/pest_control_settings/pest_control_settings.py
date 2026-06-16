# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PestControlSettings(Document):
    def validate(self):
        self.validate_diameter_unit()
        self.validate_default_division_types()

    def validate_diameter_unit(self):
        if not self.check_visit_location_remoteness:
            return
        valid_uoms = {row[0] for row in _query_uoms_by_category("Length")}
        if self.diameter_unit not in valid_uoms:
            frappe.throw(
                frappe._("{0} is not a valid Length unit").format(
                    frappe.bold(self.diameter_unit))
            )

    def validate_default_division_types(self):
        for row in self.default_division_types:
            country = frappe.db.get_value(
                "Address Division Type", row.division_type, "country")
            if country != row.country:
                frappe.throw(
                    frappe._(
                        "Row #{0}: Division Type {1} does not belong to country {2}"
                    ).format(row.idx, frappe.bold(row.division_type), frappe.bold(row.country))
                )


def _query_uoms_by_category(category: str, txt: str = "", page_len: int = 500, start: int = 0):
    UCF = frappe.qb.DocType("UOM Conversion Factor")
    return (
        frappe.qb.from_(UCF)
        .select(UCF.to_uom)
        .distinct()
        .where(UCF.category == category)
        .where(UCF.to_uom.like(f"%{txt}%"))
        .limit(page_len)
        .offset(start)
        .run()
    )


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_uoms_by_category(doctype, txt, searchfield, start, page_len, filters):
    category = (filters or {}).get("category", "Length")
    return _query_uoms_by_category(category, txt=txt, page_len=page_len, start=start)
