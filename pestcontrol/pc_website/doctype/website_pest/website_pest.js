// Copyright (c) 2026, QualityPoint and contributors
// For license information, please see license.txt

frappe.ui.form.on("Website Pest", {
	setup(frm) {
		frm.set_query("pest_type", () => ({
			query: "pestcontrol.pc_setup.doctype.pest_category.pest_category.pest_type_by_category",
			filters: { category: frm.doc.category },
		}));
	},

	category(frm) {
		// the previously chosen pest_type may no longer belong to the new category
		if (frm.doc.pest_type) {
			frm.set_value("pest_type", null);
		}
	},
});
