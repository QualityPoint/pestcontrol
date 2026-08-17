// Copyright (c) 2026, QualityPoint and contributors
// For license information, please see license.txt

frappe.provide("pestcontrol");

pestcontrol.PESTS_FOR_CATEGORIES_METHOD =
	"pestcontrol.pc_setup.doctype.pest_category.pest_category.get_pest_types_for_categories";

// how stored values are joined in the Small Text fields (readable as a grid column)
pestcontrol.PILL_SEP = ", ";

/**
 * Simulate two "Table MultiSelect" fields *inside a child-table row* — which
 * Frappe forbids (no grandchild tables). Each is a `MultiSelectPills` control
 * (the same pills UI a real Table MultiSelect uses) hosted in an HTML field and
 * persisted to a `Small Text` field as a comma-joined string (the same trick
 * `transaction_naming_html` uses). Because the value lives in a real field, that
 * field can be `reqd` and shown in the grid/list view.
 *
 * Selecting categories MERGES their pest types into the pest-types pills — the
 * "facilitate selection by category" behavior, reusing the Pest Category model.
 *
 * @param {string} child_doctype  e.g. "Visit Facility Item"
 * @param {string} grid_field     parent's table fieldname, e.g. "amenities"
 */
pestcontrol.bind_amenity_pest_editors = function (child_doctype, grid_field) {
	frappe.ui.form.on(child_doctype, {
		form_render(frm, cdt, cdn) {
			pestcontrol.mount_amenity_pest_row(frm, cdt, cdn, grid_field);
		},
	});
};

pestcontrol.mount_amenity_pest_row = function (frm, cdt, cdn, grid_field) {
	const grid_row = frm.fields_dict[grid_field]?.grid?.grid_rows_by_docname[cdn];
	if (!grid_row || !grid_row.grid_form) return;

	const type_ctrl = pestcontrol._mount_row_pills(grid_row, cdt, cdn, {
		html_field: "pest_type_html",
		store_field: "pest_type",
		link_doctype: "Pest Type",
		search_filters: { disabled: 0 }, // exclude retired pest types
	});

	pestcontrol._mount_row_pills(grid_row, cdt, cdn, {
		html_field: "pest_category_html",
		store_field: "pest_category",
		link_doctype: "Pest Category",
		on_change: (categories) => {
			if (!categories.length || !type_ctrl) return;
			frappe.xcall(pestcontrol.PESTS_FOR_CATEGORIES_METHOD, { categories }).then((pests) => {
				const merged = Array.from(new Set([...(type_ctrl.get_values() || []), ...pests]));
				type_ctrl.set_formatted_input(merged); // update pills, no change event
				frappe.model.set_value(cdt, cdn, "pest_type", merged.join(pestcontrol.PILL_SEP));
			});
		},
	});
};

pestcontrol._mount_row_pills = function (grid_row, cdt, cdn, opts) {
	const field = grid_row.grid_form.fields_dict[opts.html_field];
	if (!field) return null;

	const $wrapper = $(field.$wrapper || field.wrapper).empty();
	const row = locals[cdt][cdn];

	// space before the next field's label (padding doesn't collapse like margin)
	$wrapper.css("padding-bottom", "var(--margin-md)");

	// HTML fields never render their own label, so add one ourselves.
	if (field.df.label) {
		$('<label class="control-label" style="display:block;">')
			.text(__(field.df.label))
			.appendTo($wrapper);
	}

	const control = frappe.ui.form.make_control({
		parent: $wrapper,
		df: {
			fieldtype: "MultiSelectPills",
			fieldname: opts.store_field + "_pills",
			// native link search: server-side filtering + relevance, and it
			// translates labels for `translated_doctype` while keeping the real
			// name as the value.
			get_data: (txt) => {
				const args = { doctype: opts.link_doctype, txt: txt || "" };
				// only send filters when present; null becomes "" server-side and
				// breaks json.loads in search_widget
				if (opts.search_filters) {
					args.filters = JSON.stringify(opts.search_filters);
				}
				return frappe.xcall("frappe.desk.search.search_link", args).then((results) =>
					results.map((d) => ({
						value: d.value,
						label: d.label || __(d.value),
						description: d.description,
					}))
				);
			},
			change: () => {
				const values = control.get_values() || [];
				frappe.model.set_value(
					cdt,
					cdn,
					opts.store_field,
					values.join(pestcontrol.PILL_SEP)
				);
				opts.on_change && opts.on_change(values);
			},
		},
		render_input: true,
		only_input: true, // suppress the control's own (empty) label slot
	});

	// click a pill's label to open its linked document (route by the real name)
	if (opts.link_doctype) {
		pestcontrol._inject_pill_styles();
		control.$wrapper.addClass("pest-link-pills");
		$wrapper.on("click", ".btn-link-to-form", (e) => {
			e.preventDefault();
			const $pill = $(e.currentTarget).closest(".tb-selected-value");
			const name = decodeURIComponent($pill.attr("data-value") || "");
			if (name) frappe.set_route("Form", opts.link_doctype, name);
		});
	}

	// seed from the stored value WITHOUT firing change (opening a row stays clean)
	const current = (row[opts.store_field] || "").split(/\s*[\n,]\s*/).filter(Boolean);
	control.set_formatted_input(current);

	return control;
};

// underline a clickable pill's label on hover (injected once)
pestcontrol._inject_pill_styles = function () {
	if (document.getElementById("pest-link-pills-style")) return;
	$(`<style id="pest-link-pills-style">
		.pest-link-pills .data-pill { cursor: pointer; }
		.pest-link-pills .data-pill:hover .btn-link-to-form { text-decoration: underline; }
	</style>`).appendTo(document.head);
};
