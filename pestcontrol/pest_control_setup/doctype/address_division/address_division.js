// Copyright (c) 2026, QP and contributors
// For license information, please see license.txt

frappe.ui.form.on("Address Division", {
    setup(frm) {
        frm.set_query("parent_division", function () {
            return {
                filters: {
                    is_group: 1,
                    country: frm.doc.country,
                }
            };
        });
    },

    division_type(frm) {
        frm.set_value("parent_division", "");
        if (!frm.doc.division_type) {
            frm.set_query("parent_division", function () {
                return { filters: { is_group: 1, country: frm.doc.country } };
            });
            return;
        }
        frappe.call({
            method: "pestcontrol.pest_control_setup.doctype.address_division.address_division.get_parent_division_type",
            args: { division_type: frm.doc.division_type },
            callback(r) {
                let filters = {
                    is_group: 1,
                    country: frm.doc.country
                };
                if (r.message) {
                    filters.division_type = r.message;
                }
                frm.set_query("parent_division", function () {
                    return { filters };
                });
            },
        });
    },
});
