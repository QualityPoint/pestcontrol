frappe.treeview_settings["Operation Team Member"] = {
    get_tree_nodes: "pestcontrol.operation.doctype.operation_team_member.operation_team_member.get_children",
    filters: [
        {
            fieldname: "company",
            fieldtype: "Select",
            options: ["All Companies"].concat(erpnext.utils.get_tree_options("company")),
            label: __("Company"),
            default: erpnext.utils.get_tree_default("company"),
        },
    ],
    breadcrumb: "Operation",
    disable_add_node: true,
    get_tree_root: false,
    toolbar: [
        { toggle_btn: true },
        {
            label: __("Edit"),
            condition: function (node) {
                return !node.is_root;
            },
            click: function (node) {
                frappe.set_route("Form", "Operation Team Member", node.data.value);
            },
        },
    ],
    menu_items: [
        {
            label: __("New Operation Team Member"),
            action: function () {
                frappe.new_doc("Operation Team Member", true);
            },
            condition: 'frappe.boot.user.can_create.indexOf("Operation Team Member") !== -1',
        },
    ],
};
