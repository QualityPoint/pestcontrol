// Copyright (c) 2026, QP and contributors
// For license information, please see license.txt

frappe.ui.form.on("Address Division Type", {
    setup(frm) {
        frm.set_query("parent_division_type", function () {
            return {
                filters: {
                    is_group: 1,
                    country: frm.doc.country
                }
            };
        });
    },
});
