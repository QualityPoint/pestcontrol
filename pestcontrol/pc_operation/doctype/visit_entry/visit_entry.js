// Copyright (c) 2026, QP and contributors
// For license information, please see license.txt

// Mount the per-row pest-type / pest-category multi-select pills inside the
// amenities child table (see utilities/visit_facility_item.js).
pestcontrol.bind_amenity_pest_editors("Visit Facility Item", "amenities");

frappe.ui.form.on("Visit Entry", {
	setup(frm) {
		frm.set_query("operation_order", function () {
			return {
				filters: {
					company: frm.doc.company,
					customer: frm.doc.customer,
					docstatus: 1,
				},
			};
		});

		frm.set_query("supervisor", function () {
			return {
				filters: {
					company: frm.doc.company,
					is_supervisor: 1,
				},
			};
		});

		frm.set_query("worker", "workers", function () {
			return {
				filters: {
					company: frm.doc.company,
				},
			};
		});

		// Restrict each chemical's UOM to the item's configured UOMs, the same
		// way ERPNext does (gated by Stock Settings →
		// "Allow UOM with conversion rate defined in Item").
		frm.set_query("uom", "chemicals", function (doc, cdt, cdn) {
			const row = locals[cdt][cdn];
			return {
				query: "erpnext.controllers.queries.get_item_uom_query",
				filters: {
					item_code: row.chemical_item,
				},
			};
		});
	},
	customer(frm) {
		// Clear the order link when the customer changes, to avoid confusion.
		frm.set_value("operation_order", null);
	},
	company(frm) {
		// Clear the order link when the company changes, to avoid confusion.
		frm.set_value("operation_order", null);
	},
});

// Live preview only — the server recomputes all of this authoritatively in
// VisitEntry.before_submit (durations + totals).

// Recompute one row's read-only `duration`; returns the promise so callers
// can chain a roll-up once the value is set.
function update_row_duration(frm, cdt, cdn) {
	const row = locals[cdt][cdn];
	return pestcontrol.utils
		.calculate_duration(row.from_time, row.to_time)
		.then((seconds) => frappe.model.set_value(cdt, cdn, "duration", seconds));
}

// Roll up the timesheet intervals into the read-only visit summary fields.
// Mirrors VisitEntry.set_visit_totals on the server.
function update_visit_totals(frm) {
	const rows = frm.doc.timesheet || [];
	const visit_duration = rows.reduce((total, r) => total + (r.duration || 0), 0);

	const starts = rows.filter((r) => r.from_time).map((r) => moment(r.from_time));
	const ends = rows.filter((r) => r.to_time).map((r) => moment(r.to_time));
	let visit_timeout = 0;
	if (starts.length && ends.length) {
		const span = moment.max(ends).diff(moment.min(starts), "seconds");
		visit_timeout = Math.max(span - visit_duration, 0);
	}

	frm.set_value({ interval_count: rows.length, visit_duration, visit_timeout });
}

// timesheet rows feed the visit totals; worker rows only need their own duration
function update_timesheet_row(frm, cdt, cdn) {
	update_row_duration(frm, cdt, cdn).then(() => update_visit_totals(frm));
}

frappe.ui.form.on("Visit Timesheet", {
	from_time: update_timesheet_row,
	to_time: update_timesheet_row,
	timesheet_add: update_visit_totals,
	timesheet_remove: update_visit_totals,
});

frappe.ui.form.on("Visit Operation Worker", {
	from_time: update_row_duration,
	to_time: update_row_duration,
});

// Chemicals: resolve UOM conversion the ERPNext way. chemical_name & stock_uom
// arrive via fetch_from; here we default the UOM to the item's stock UOM and
// pull the conversion factor (the server recomputes it authoritatively).
frappe.ui.form.on("Visit Chemical Item", {
	chemical_item(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (!row.chemical_item) return;
		// default the transaction UOM to sales_uom (fallback stock_uom), exactly
		// like Delivery Note (erpnext get_item_details)
		frappe.db.get_value("Item", row.chemical_item, ["sales_uom", "stock_uom"]).then((r) => {
			const m = r.message || {};
			const uom = m.sales_uom || m.stock_uom;
			if (uom) frappe.model.set_value(cdt, cdn, "uom", uom);
		});
	},
	uom(frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		if (!row.chemical_item || !row.uom) return;
		frappe
			.xcall("erpnext.stock.get_item_details.get_conversion_factor", {
				item_code: row.chemical_item,
				uom: row.uom,
			})
			.then((r) =>
				frappe.model.set_value(cdt, cdn, "conversion_factor", r.conversion_factor || 0)
			);
	},
});
