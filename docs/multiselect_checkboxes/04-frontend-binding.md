# 04 · Frontend — binding the widget onto forms

> Concern: **wiring**. How the `ItemEditor` from [03](03-frontend-editor.md) is
> mounted on the Profile form and on Consumer forms, including the dual‑mode
> lock. The reusable binder keeps every doctype's `.js` to a single line (DRY).

## A. The Profile form (manual mode only)

The Profile form authors a bundle — the grid is always editable. Mirrors
`role_profile.js`.

```js
// myapp/.../doctype/profile/profile.js
frappe.ui.form.on("Profile", {
    refresh(frm) {
        if (has_common(frappe.user_roles, ["Administrator", "System Manager"])) {
            if (!frm.item_editor) {
                const area = $(frm.fields_dict.items_html.wrapper);
                frm.item_editor = new myapp.ItemEditor(area, frm); // defaults: items / item / Item Link
            }
            frm.item_editor.show();
        }
    },
    validate(frm) {
        if (frm.item_editor) frm.item_editor.set_values_in_table();
    },
});
```

> `validate` flushes the grid into the hidden table **before save** — essential,
> because `on_change` covers clicks but `validate` guarantees a final sync.

## B. The reusable Consumer binder (DRY)

Every Consumer needs the same dual‑mode logic, so put it in the bundle **once**
and expose a one‑line binder. Mirrors how core keeps logic in `RoleEditor`.

```js
// myapp/public/js/components/profile_editor.js
frappe.provide("myapp");

myapp.ITEM_EDITOR_ROLES = ["Administrator", "System Manager"]; // who may edit

/**
 * Wire the dual-mode editor onto a Consumer doctype.
 * @param {string} parent_doctype          e.g. "Sales Order"
 * @param {string} profile_child_doctype   the Table MultiSelect child, e.g. "Profile Link"
 * @param {string} item_child_doctype      the hidden items child, e.g. "Item Link"
 */
myapp.bind_profile_editor = function (parent_doctype, profile_child_doctype, item_child_doctype) {
    frappe.ui.form.on(parent_doctype, {
        refresh: (frm) => myapp.setup_item_editor(frm, item_child_doctype),
        validate: (frm) => frm.item_editor && frm.item_editor.set_values_in_table(),
    });

    frappe.ui.form.on(profile_child_doctype, {
        profiles_add: (frm) => myapp.toggle_item_editor_lock(frm),
        profiles_remove: (frm) => myapp.toggle_item_editor_lock(frm),
    });
};

myapp.setup_item_editor = function (frm, item_child_doctype) {
    if (frm.doc.docstatus !== 0) return;                              // editable only in draft
    if (!has_common(frappe.user_roles, myapp.ITEM_EDITOR_ROLES)) return;

    const has_profiles = (frm.doc.profiles || []).length > 0;

    if (!frm.item_editor) {
        const area = $(frm.fields_dict.items_html.wrapper);
        frm.item_editor = new myapp.ItemEditor(area, frm, has_profiles ? 1 : 0, {
            table_fieldname: "items",
            value_fieldname: "item",
            child_doctype: item_child_doctype,
        });
    } else {
        frm.item_editor.disable = has_profiles ? 1 : 0;
    }
    frm.item_editor.show();
};

myapp.toggle_item_editor_lock = function (frm) {
    if (!frm.item_editor) return;
    if ((frm.doc.profiles || []).length > 0) {
        frm.item_editor.disable = 1;                                 // lock manual editing
        frm.call("populate_profile_items").then(() => frm.item_editor.show()); // expand server-side
    } else {
        frm.item_editor.disable = 0;                                 // re-enable manual mode
        frm.item_editor.show();
    }
};
```

Register it in the bundle:

```js
// myapp.bundle.js
import "./components/item_editor.js";
import "./components/profile_editor.js";
```

## C. Each Consumer's form script — one line

```js
// myapp/.../doctype/sales_order/sales_order.js
myapp.bind_profile_editor("Sales Order", "Profile Link", "Item Link");
```

Adding a new consuming doctype later is now a single declarative call — no
copy‑paste.

## The child‑table event naming rule

The add/remove handlers are registered on the **child doctype**, but named after
the **parent field**:

```js
frappe.ui.form.on(<child doctype>, { <parent_fieldname>_add, <parent_fieldname>_remove });
```

Here the Consumer's field is `profiles` and the child doctype is `Profile Link`,
so the events are `profiles_add` / `profiles_remove`. Mirrors core's
`frappe.ui.form.on("User Role Profile", { role_profiles_add, role_profiles_remove })`.

## Dual‑mode, end to end

1. **Add a profile** → `profiles_add` → `disable = 1`, server `populate_profile_items`
   rewrites `items`, then `show()` re‑renders them as disabled+checked.
2. **Remove the last profile** → `profiles_remove` → `disable = 0`, grid becomes
   editable again (existing items stay until changed).
3. **Manual ticking** (no profiles) → `on_change`/`validate` → `set_values_in_table`.
4. **Save** → server `validate()` is authoritative (see [05](05-backend.md)).

> Note: locked checkboxes still report their checked state, so the `validate`
> sync during profile mode simply reproduces the server‑derived set — harmless.
