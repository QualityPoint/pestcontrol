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
    },
});
