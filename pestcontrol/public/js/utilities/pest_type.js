// Copyright (c) 2026, QP and contributors
// For license information, please see license.txt

frappe.provide("pestcontrol");

/**
 * A MultiCheck grid editor that syncs checked options into a hidden child table.
 *
 * Modeled on frappe.RoleEditor: the visible widget (an HTML field) is decoupled
 * from the hidden, read-only child table that actually stores the data. The grid
 * is the only thing the user touches; on every change (and on validate) the
 * selection is written back into the child table.
 *
 * @param {JQuery|HTMLElement} wrapper Container for the MultiCheck control.
 * @param {frappe.ui.form.Form} frm Form whose child rows are edited.
 * @param {boolean|number|Object} [disable=false] Lock the grid (read-only), or pass options here.
 * @param {Object} [options] Configuration overrides.
 * @param {string} [options.table_fieldname="pests"] Child table field holding the rows.
 * @param {string} [options.value_fieldname="pest_type"] Field in each child row storing the value.
 * @param {string} [options.child_doctype="Pest Item"] Child DocType used when adding rows.
 * @param {string} [options.data_method] Whitelisted method returning the selectable values.
 */
pestcontrol.PestTypeEditor = class {
	constructor(wrapper, frm, disable = false, options = {}) {
		if (disable && typeof disable === "object") {
			options = disable;
			disable = false;
		}

		const {
			table_fieldname = "pests",
			value_fieldname = "pest_type",
			child_doctype = "Pest Item",
			data_method = "pestcontrol.pc_setup.doctype.pest_category.pest_category.get_all_pest_types",
		} = options;

		this.frm = frm;
		this.wrapper = wrapper;
		this.disable = Boolean(disable);
		this.table_fieldname = table_fieldname;
		this.value_fieldname = value_fieldname;
		this.child_doctype = child_doctype;
		this.data_method = data_method;

		let selected = this.get_selected_values();
		this.multicheck = frappe.ui.form.make_control({
			parent: wrapper,
			df: {
				fieldname: this.table_fieldname,
				fieldtype: "MultiCheck",
				select_all: true,
				columns: "15rem",
				get_data: () => {
					return frappe.xcall(this.data_method).then((values) => {
						return values.map((value) => {
							return {
								label: __(value),
								value: value,
								checked: selected.includes(value),
							};
						});
					});
				},
				on_change: () => {
					this.set_values_in_table();
					this.frm.dirty();
				},
			},
			render_input: true,
		});

		// re-apply the disabled state whenever the checkbox grid re-renders
		let original_make_checkboxes = this.multicheck.make_checkboxes;
		this.multicheck.make_checkboxes = () => {
			original_make_checkboxes.call(this.multicheck);
			this.set_enable_disable();
		};
	}

	set_enable_disable() {
		$(this.wrapper)
			.find('input[type="checkbox"]')
			.attr("disabled", this.disable ? true : false);
		$(this.wrapper)
			.find(".select-all, .deselect-all")
			.prop("disabled", this.disable ? true : false);
	}

	show() {
		this.reset();
		this.set_enable_disable();
	}

	reset() {
		this.multicheck.selected_options = this.get_selected_values();
		this.multicheck.refresh_input();
	}

	set_values_in_table() {
		let rows = this.get_rows();
		let checked_options = this.multicheck.get_checked_options();

		// drop rows that are no longer checked
		rows.forEach((row) => {
			if (!checked_options.includes(row[this.value_fieldname])) {
				frappe.model.clear_doc(row.doctype, row.name);
			}
		});

		// add rows for newly checked options
		checked_options.forEach((value) => {
			if (!rows.find((d) => d[this.value_fieldname] === value)) {
				let row = frappe.model.add_child(
					this.frm.doc,
					this.child_doctype,
					this.table_fieldname
				);
				row[this.value_fieldname] = value;
			}
		});
	}

	get_rows() {
		return this.frm.doc[this.table_fieldname] || [];
	}

	get_selected_values() {
		return this.get_rows().map((row) => row[this.value_fieldname]);
	}
};
