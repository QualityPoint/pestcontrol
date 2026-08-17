// Copyright (c) 2026, QualityPoint and contributors
// For license information, please see license.txt

frappe.ui.form.on("Visit Request", {
	setup(frm) {
		frm.set_query("company", () => {
			return {
				filters: {
					is_group: 0,
				},
			};
		});

		frm.set_query("operation_order", () => {
			return {
				filters: {
					company: frm.doc.company,
					customer: frm.doc.customer,
				},
			};
		});

		frm.set_query("visit_entry", () => {
			return {
				filters: {
					company: frm.doc.company,
					customer: frm.doc.customer,
					operation_order: frm.doc.operation_order,
				},
			};
		});

		frm.set_query("assigned_supervisor", () => {
			return {
				filters: {
					company: frm.doc.company,
					is_supervisor: 1,
				},
			};
		});
	},
});
