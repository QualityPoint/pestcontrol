// Copyright (c) 2026, QP and contributors
// For license information, please see license.txt

frappe.ui.form.on("Operation Worker", {
    setup(frm) {
        frm.set_query("worker", function () {
            return {
                filters: {
                    company: frm.doc.company,
                    status: "Active"
                }
            };
        });
    },
});
