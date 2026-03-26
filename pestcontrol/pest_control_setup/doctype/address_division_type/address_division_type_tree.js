// Copyright (c) 2026, QP and contributors
// For license information, please see license.txt

frappe.treeview_settings["Address Division Type"] = {
    get_tree_nodes: "pestcontrol.pest_control_setup.doctype.address_division_type.address_division_type.get_children",
    add_tree_node: "pestcontrol.pest_control_setup.doctype.address_division_type.address_division_type.add_node",
    filters: [
        {
            fieldname: "country",
            fieldtype: "Link",
            options: "Country",
            label: __("Country"),
            default: frappe.defaults.get_default("country"),
        },
    ],
    breadcrumb: "Operation",
    get_tree_root: false,
    extend_toolbar: true,
    toolbar: [
        {
            label: __("Edit"),
            condition: function (node) {
                return !node.is_root;
            },
            click: function (node) {
                frappe.set_route("Form", "Address Division Type", node.data.value);
            },
        },
    ],
    menu_items: [
        {
            label: __("New Address Division Type"),
            action: function () {
                frappe.new_doc("Address Division Type", true);
            },
            condition: 'frappe.boot.user.can_create.indexOf("Address Division Type") !== -1',
        },
    ],
};