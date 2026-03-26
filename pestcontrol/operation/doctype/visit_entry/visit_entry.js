// Copyright (c) 2026, QP and contributors
// For license information, please see license.txt

frappe.ui.form.on("Visit Entry", {
    setup(frm) {
        frm.set_query("project", function () {
            return {
                filters: {
                    company: frm.doc.company,
                    customer: frm.doc.customer
                }
            };
        });

        frm.set_query("operation_supervisor", function () {
            return {
                filters: {
                    company: frm.doc.company,
                    is_supervisor: 1
                }
            };
        });

        frm.set_query("team_member", "team_members", function () {
            return {
                filters: {
                    company: frm.doc.company,
                }
            };
        });
    },
});
