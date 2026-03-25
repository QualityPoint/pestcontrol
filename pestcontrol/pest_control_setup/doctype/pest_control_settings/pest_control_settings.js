// Copyright (c) 2026, QP and contributors
// For license information, please see license.txt

frappe.ui.form.on("Pest Control Settings", {
    setup(frm) {
        frm.set_query("diameter_unit", function () {
            return {
                query: "pestcontrol.pest_control_setup.doctype.pest_control_settings.pest_control_settings.get_uoms_by_category",
                filters: {
                    category: "Length"
                }
            };
        });
    },
});
