// Copyright (c) 2026, QP and contributors
// For license information, please see license.txt

frappe.ui.form.on("Operation Visit", {
    setup(frm) {
        frm.set_query("project", function () {
            return {
                filters: {
                    customer: frm.doc.customer
                }
            };
        });

        frm.set_query("operation_supervisor", function () {
            return {
                filters: {
                    is_supervisor: 1
                }
            };
        });
    },
});
