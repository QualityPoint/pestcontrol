(() => {
  // ../pestcontrol/pestcontrol/public/js/utilities/filters.js
  frappe.provide("pestcontrol.filters");
  pestcontrol.filters = {};

  // ../pestcontrol/pestcontrol/public/js/utilities/utils.js
  frappe.provide("pestcontrol.utils");
  pestcontrol.utils = {
    calculate_duration(from_time, to_time) {
      if (!from_time || !to_time)
        return Promise.resolve(0);
      return frappe.xcall("pestcontrol.utils.calculate_duration", { from_time, to_time });
    }
  };

  // ../pestcontrol/pestcontrol/public/js/utilities/queries.js
  frappe.provide("pestcontrol.queries");
  pestcontrol.queries = {};

  // ../pestcontrol/pestcontrol/public/js/utilities/pest_type.js
  frappe.provide("pestcontrol");
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
        data_method = "pestcontrol.pc_setup.doctype.pest_category.pest_category.get_all_pest_types"
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
                  value,
                  checked: selected.includes(value)
                };
              });
            });
          },
          on_change: () => {
            this.set_values_in_table();
            this.frm.dirty();
          }
        },
        render_input: true
      });
      let original_make_checkboxes = this.multicheck.make_checkboxes;
      this.multicheck.make_checkboxes = () => {
        original_make_checkboxes.call(this.multicheck);
        this.set_enable_disable();
      };
    }
    set_enable_disable() {
      $(this.wrapper).find('input[type="checkbox"]').attr("disabled", this.disable ? true : false);
      $(this.wrapper).find(".select-all, .deselect-all").prop("disabled", this.disable ? true : false);
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
      rows.forEach((row) => {
        if (!checked_options.includes(row[this.value_fieldname])) {
          frappe.model.clear_doc(row.doctype, row.name);
        }
      });
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

  // ../pestcontrol/pestcontrol/public/js/utilities/pest_category.js
  frappe.provide("pestcontrol");
  pestcontrol.PEST_EDITOR_ROLES = ["Administrator", "System Manager", "Project Master Manager"];
  pestcontrol.bind_pest_category_editor = function(parent_doctype, category_child_doctype, pest_child_doctype) {
    frappe.ui.form.on(parent_doctype, {
      refresh: (frm) => pestcontrol.setup_pest_editor(frm, pest_child_doctype),
      validate: (frm) => frm.pest_editor && frm.pest_editor.set_values_in_table()
    });
    frappe.ui.form.on(category_child_doctype, {
      pest_category_add: (frm) => pestcontrol.toggle_pest_editor_lock(frm),
      pest_category_remove: (frm) => pestcontrol.toggle_pest_editor_lock(frm)
    });
  };
  pestcontrol.setup_pest_editor = function(frm, pest_child_doctype) {
    if (frm.doc.docstatus !== 0)
      return;
    if (!has_common(frappe.user_roles, pestcontrol.PEST_EDITOR_ROLES))
      return;
    const has_categories = (frm.doc.pest_category || []).length > 0;
    if (!frm.pest_editor) {
      const pest_area = $(frm.fields_dict.pests_html.wrapper);
      frm.pest_editor = new pestcontrol.PestTypeEditor(pest_area, frm, has_categories ? 1 : 0, {
        table_fieldname: "pests",
        value_fieldname: "pest_type",
        child_doctype: pest_child_doctype
      });
    } else {
      frm.pest_editor.disable = has_categories ? 1 : 0;
    }
    frm.pest_editor.show();
  };
  pestcontrol.toggle_pest_editor_lock = function(frm) {
    if (!frm.pest_editor)
      return;
    if ((frm.doc.pest_category || []).length > 0) {
      frm.pest_editor.disable = 1;
      frm.call("populate_category_pests").then(() => frm.pest_editor.show());
    } else {
      frm.pest_editor.disable = 0;
      frm.pest_editor.show();
    }
  };

  // ../pestcontrol/pestcontrol/public/js/utilities/visit_facility_item.js
  frappe.provide("pestcontrol");
  pestcontrol.PESTS_FOR_CATEGORIES_METHOD = "pestcontrol.pc_setup.doctype.pest_category.pest_category.get_pest_types_for_categories";
  pestcontrol.PILL_SEP = ", ";
  pestcontrol.bind_amenity_pest_editors = function(child_doctype, grid_field) {
    frappe.ui.form.on(child_doctype, {
      form_render(frm, cdt, cdn) {
        pestcontrol.mount_amenity_pest_row(frm, cdt, cdn, grid_field);
      }
    });
  };
  pestcontrol.mount_amenity_pest_row = function(frm, cdt, cdn, grid_field) {
    var _a, _b;
    const grid_row = (_b = (_a = frm.fields_dict[grid_field]) == null ? void 0 : _a.grid) == null ? void 0 : _b.grid_rows_by_docname[cdn];
    if (!grid_row || !grid_row.grid_form)
      return;
    const type_ctrl = pestcontrol._mount_row_pills(grid_row, cdt, cdn, {
      html_field: "pest_type_html",
      store_field: "pest_type",
      link_doctype: "Pest Type",
      search_filters: { disabled: 0 }
    });
    pestcontrol._mount_row_pills(grid_row, cdt, cdn, {
      html_field: "pest_category_html",
      store_field: "pest_category",
      link_doctype: "Pest Category",
      on_change: (categories) => {
        if (!categories.length || !type_ctrl)
          return;
        frappe.xcall(pestcontrol.PESTS_FOR_CATEGORIES_METHOD, { categories }).then((pests) => {
          const merged = Array.from(
            /* @__PURE__ */ new Set([...type_ctrl.get_values() || [], ...pests])
          );
          type_ctrl.set_formatted_input(merged);
          frappe.model.set_value(cdt, cdn, "pest_type", merged.join(pestcontrol.PILL_SEP));
        });
      }
    });
  };
  pestcontrol._mount_row_pills = function(grid_row, cdt, cdn, opts) {
    const field = grid_row.grid_form.fields_dict[opts.html_field];
    if (!field)
      return null;
    const $wrapper = $(field.$wrapper || field.wrapper).empty();
    const row = locals[cdt][cdn];
    $wrapper.css("padding-bottom", "var(--margin-md)");
    if (field.df.label) {
      $('<label class="control-label" style="display:block;">').text(__(field.df.label)).appendTo($wrapper);
    }
    const control = frappe.ui.form.make_control({
      parent: $wrapper,
      df: {
        fieldtype: "MultiSelectPills",
        fieldname: opts.store_field + "_pills",
        get_data: (txt) => {
          const args = { doctype: opts.link_doctype, txt: txt || "" };
          if (opts.search_filters) {
            args.filters = JSON.stringify(opts.search_filters);
          }
          return frappe.xcall("frappe.desk.search.search_link", args).then(
            (results) => results.map((d) => ({
              value: d.value,
              label: d.label || __(d.value),
              description: d.description
            }))
          );
        },
        change: () => {
          const values = control.get_values() || [];
          frappe.model.set_value(cdt, cdn, opts.store_field, values.join(pestcontrol.PILL_SEP));
          opts.on_change && opts.on_change(values);
        }
      },
      render_input: true,
      only_input: true
    });
    if (opts.link_doctype) {
      pestcontrol._inject_pill_styles();
      control.$wrapper.addClass("pest-link-pills");
      $wrapper.on("click", ".btn-link-to-form", (e) => {
        e.preventDefault();
        const $pill = $(e.currentTarget).closest(".tb-selected-value");
        const name = decodeURIComponent($pill.attr("data-value") || "");
        if (name)
          frappe.set_route("Form", opts.link_doctype, name);
      });
    }
    const current = (row[opts.store_field] || "").split(/\s*[\n,]\s*/).filter(Boolean);
    control.set_formatted_input(current);
    return control;
  };
  pestcontrol._inject_pill_styles = function() {
    if (document.getElementById("pest-link-pills-style"))
      return;
    $(`<style id="pest-link-pills-style">
		.pest-link-pills .data-pill { cursor: pointer; }
		.pest-link-pills .data-pill:hover .btn-link-to-form { text-decoration: underline; }
	</style>`).appendTo(document.head);
  };
})();
//# sourceMappingURL=pestcontrol.bundle.HIDDIFTO.js.map
