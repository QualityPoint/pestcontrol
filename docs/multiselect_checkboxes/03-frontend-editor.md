# 03 · Frontend — the `ItemEditor` widget

> Concern: the **editing UI** only. This widget renders a checkbox grid into an
> HTML field and syncs ticks into a hidden child table. It knows nothing about
> profiles or expansion — that is layer [04](04-frontend-binding.md) / [05](05-backend.md).

## Where it lives (load order matters)

Put the widget in your app's **global desk bundle** so it is defined before any
form loads — exactly how Frappe ships `RoleEditor` in core JS.

```js
// myapp/public/js/myapp.bundle.js
import "./components/item_editor.js";
```

```python
# myapp/hooks.py
app_include_js = "myapp.bundle.js"
```

After adding/editing bundle files you **must** run `bench build --app myapp`.

## The widget

```js
// myapp/public/js/components/item_editor.js
frappe.provide("myapp");

/**
 * MultiCheck grid that syncs checked options into a hidden child table.
 *
 * @param {JQuery|HTMLElement} wrapper  Container (the HTML field's wrapper).
 * @param {frappe.ui.form.Form} frm     The form being edited.
 * @param {boolean|number|Object} [disable=false]  Lock the grid, OR pass options here.
 * @param {Object} [options]
 * @param {string} [options.table_fieldname="items"]  Hidden child table field.
 * @param {string} [options.value_fieldname="item"]   Link field inside each child row.
 * @param {string} [options.child_doctype="Item Link"] Child doctype to add rows of.
 * @param {string} [options.data_method]  Whitelisted dotted path returning selectable values.
 */
myapp.ItemEditor = class {
    constructor(wrapper, frm, disable = false, options = {}) {
        // allow (wrapper, frm, options) when no disable flag is needed
        if (disable && typeof disable === "object") {
            options = disable;
            disable = false;
        }

        const {
            table_fieldname = "items",
            value_fieldname = "item",
            child_doctype = "Item Link",
            data_method = "myapp.path.to.profile.get_all_items",
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
                    return frappe.xcall(this.data_method).then((values) =>
                        values.map((value) => ({
                            label: __(value),
                            value: value,
                            checked: selected.includes(value),
                        }))
                    );
                },
                on_change: () => {
                    this.set_values_in_table();
                    this.frm.dirty();
                },
            },
            render_input: true,
        });

        // re-apply disabled state every time the grid re-renders
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
        let checked = this.multicheck.get_checked_options();

        // remove rows that are no longer checked
        rows.forEach((row) => {
            if (!checked.includes(row[this.value_fieldname])) {
                frappe.model.clear_doc(row.doctype, row.name);
            }
        });

        // add rows for newly checked options
        checked.forEach((value) => {
            if (!rows.find((d) => d[this.value_fieldname] === value)) {
                let row = frappe.model.add_child(this.frm.doc, this.child_doctype, this.table_fieldname);
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
```

## Method responsibilities

| Method | Does |
|---|---|
| `constructor` | Builds a `MultiCheck` control inside `wrapper`; `get_data` fetches selectable values from the server; wires `on_change` to sync + dirty the form. |
| `set_values_in_table` | **The bridge.** Reads checked boxes → adds/removes rows in the hidden child table via `frappe.model.add_child` / `clear_doc`. |
| `reset` | Re‑syncs the grid's checked state from the current table rows and re‑renders. Call after the table changes underneath the widget. |
| `set_enable_disable` | Toggles the `disabled` attribute on checkboxes and the select/deselect‑all buttons. |
| `show` | `reset()` + `set_enable_disable()` — the standard "redraw me" entry point. |

## Two subtleties worth knowing

1. **The `get_data` closure captures `selected` once** (at construction). That's
   fine: `reset()` updates `multicheck.selected_options` and `refresh_input()`
   re‑renders the checked state from there. So always call `show()`/`reset()`
   after you mutate the table programmatically (e.g. after server expansion).

2. **Polymorphic 3rd argument.** Passing an options object as the 3rd arg works
   (`new ItemEditor(wrapper, frm, { child_doctype: "X" })`) because the
   constructor detects an object and shifts it. Use the explicit form
   `new ItemEditor(wrapper, frm, disableFlag, options)` when you need locking.

> Common bug: the first two args are **`(wrapper, frm)`**, not `(frm, wrapper)`.
