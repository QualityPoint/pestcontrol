// Copyright (c) 2026, QP and contributors
// For license information, please see license.txt

frappe.ui.form.on("Pest Type", {
    onload: function (frm) {
        frm.list_route = "Tree/Pest Type";

        //get query select item group
        frm.fields_dict["parent_pest_type"].get_query = function (doc, cdt, cdn) {
            return {
                filters: [
                    ["Pest Type", "is_group", "=", 1],
                    ["Pest Type", "name", "!=", doc.pest_name],
                ],
            };
        };
    },

    refresh: function (frm) {
        frm.trigger("set_root_readonly");
        frm.add_custom_button(__("Pest Type Tree"), function () {
            frappe.set_route("Tree", "Pest Type");
        });
    },

    set_root_readonly: function (frm) {
        // read-only for root item group
        frm.set_intro("");
        if (!frm.doc.parent_pest_type && !frm.doc.__islocal) {
            frm.set_read_only();
            frm.set_intro(__("This is a root pest type and cannot be edited."), true);
        }
    },

    page_name: frappe.utils.warn_page_name_change,
});
