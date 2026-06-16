// Copyright (c) 2026, QP and contributors
// For license information, please see license.txt

frappe.provide("pestcontrol");

// Roles allowed to edit the pest selection on a consumer document.
pestcontrol.PEST_EDITOR_ROLES = ["Administrator", "System Manager", "Project Master Manager"];

/**
 * Wire the dual-mode pest editor onto a "consumer" doctype (the User analog):
 * a Table MultiSelect of Pest Categories that expands into a hidden `pests` table,
 * plus a manual MultiCheck grid when no category is selected.
 *
 * Collapses each consumer's form script to a single declarative call.
 *
 * @param {string} parent_doctype e.g. "Service Quotation"
 * @param {string} category_child_doctype Table MultiSelect child, e.g. "Service Pest Category"
 * @param {string} pest_child_doctype Hidden pests table child, e.g. "Service Pest Item"
 */
pestcontrol.bind_pest_category_editor = function (
	parent_doctype,
	category_child_doctype,
	pest_child_doctype
) {
	frappe.ui.form.on(parent_doctype, {
		refresh: (frm) => pestcontrol.setup_pest_editor(frm, pest_child_doctype),
		validate: (frm) => frm.pest_editor && frm.pest_editor.set_values_in_table(),
	});

	frappe.ui.form.on(category_child_doctype, {
		pest_category_add: (frm) => pestcontrol.toggle_pest_editor_lock(frm),
		pest_category_remove: (frm) => pestcontrol.toggle_pest_editor_lock(frm),
	});
};

pestcontrol.setup_pest_editor = function (frm, pest_child_doctype) {
	// pests are only editable while the document is a draft
	if (frm.doc.docstatus !== 0) return;
	if (!has_common(frappe.user_roles, pestcontrol.PEST_EDITOR_ROLES)) return;

	const has_categories = (frm.doc.pest_category || []).length > 0;

	if (!frm.pest_editor) {
		const pest_area = $(frm.fields_dict.pests_html.wrapper);
		frm.pest_editor = new pestcontrol.PestTypeEditor(pest_area, frm, has_categories ? 1 : 0, {
			table_fieldname: "pests",
			value_fieldname: "pest_type",
			child_doctype: pest_child_doctype,
		});
	} else {
		frm.pest_editor.disable = has_categories ? 1 : 0;
	}
	frm.pest_editor.show();
};

pestcontrol.toggle_pest_editor_lock = function (frm) {
	if (!frm.pest_editor) return;

	if ((frm.doc.pest_category || []).length > 0) {
		// category-driven mode: lock manual editing and expand server-side
		frm.pest_editor.disable = 1;
		frm.call("populate_category_pests").then(() => frm.pest_editor.show());
	} else {
		// no categories: re-enable manual selection
		frm.pest_editor.disable = 0;
		frm.pest_editor.show();
	}
};
