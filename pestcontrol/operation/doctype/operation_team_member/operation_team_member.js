// Copyright (c) 2026, QP and contributors
// For license information, please see license.txt

frappe.ui.form.on("Operation Team Member", {
    setup(frm) {
        frm.set_query("parent_member", function () {
            return {
                filters: {
                    is_supervisor: 1
                }
            };
        });

        frm.set_query("default_warehouse", function () {
            return {
                filters: {
                    company: frm.doc.company,
                    disabled: 0,
                    is_group: 0
                }
            };
        });
    },
});
