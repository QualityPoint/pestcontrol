// Copyright (c) 2026, QualityPoint and contributors
// For license information, please see license.txt

frappe.ui.form.on("Pest Category", {
	refresh: function (frm) {
		if (
			has_common(frappe.user_roles, [
				"Administrator",
				"System Manager",
				"Project Master Manager",
			])
		) {
			if (!frm.pest_editor) {
				const pest_area = $(frm.fields_dict.pests_html.wrapper);
				frm.pest_editor = new pestcontrol.PestTypeEditor(pest_area, frm);
			}
			frm.pest_editor.show();
		}
	},

	validate: function (frm) {
		if (frm.pest_editor) {
			frm.pest_editor.set_values_in_table();
		}
	},
});
