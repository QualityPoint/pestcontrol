# 02 · Data Model

> Create these five doctypes. Field names below become the defaults referenced
> by the widget ([03](03-frontend-editor.md)) and backend ([05](05-backend.md)).
> Keep them consistent or override them via options.

## 1. `Item` — the atomic assignable

A normal standalone doctype.

| Field | Type | Notes |
|---|---|---|
| `item_name` | Data | `reqd`, `unique`. Used as the doc name (`autoname: field:item_name`). |
| `disabled` | Check | Retired items are excluded from the grid. |

> The name (`item_name`) **is** the primary key, so junctions link to it
> directly — no ID indirection. Mirrors `Role`.

## 2. `Item Link` — the shared junction child

`istable: 1`. The single junction reused by **both** Profile and Consumer.

| Field | Type | Notes |
|---|---|---|
| `item` | Link → `Item` | The only meaningful field. |

> One junction type for both parents is the keystone of the pattern — it makes
> "copy a profile's items onto a consumer" a plain row copy. Mirrors `Has Role`.

Optional safety guard (recommended) — reject duplicate items in one parent:

```python
# item_link.py
class ItemLink(Document):
    def before_insert(self):
        if frappe.db.exists("Item Link", {"parent": self.parent, "item": self.item}):
            frappe.throw(frappe._("'{0}' already has the item '{1}'").format(self.parent, self.item))
```

## 3. `Profile` — the reusable bundle

A standalone doctype. **Three fields** that mirror Role Profile.

| Field | Type | Visibility | Purpose |
|---|---|---|---|
| `profile_name` | Data | visible | `reqd`, `unique`; `autoname: field:profile_name`. |
| `items_html` | HTML | `read_only` | Mount point for the checkbox grid. Stores nothing. |
| `items` | Table → `Item Link` | **`hidden` + `read_only`** | The bundled items (source of truth). |

The critical flags on `items`:

```json
{ "fieldname": "items", "fieldtype": "Table", "options": "Item Link",
  "hidden": 1, "read_only": 1 }
```

> `hidden` + `read_only` means the user never touches the table directly — the
> grid in `items_html` writes into it. This is the whole trick.

## 4. `Profile Link` — the profile junction child

`istable: 1`. Used by the Consumer's `Table MultiSelect`.

| Field | Type | Notes |
|---|---|---|
| `profile` | Link → `Profile` | The only field. Mirrors `User Role Profile`. |

## 5. `Consumer` — the document that assigns items

Any business doctype (order, quotation, ticket…). Add **three fields**, mirroring
the User doctype.

| Field | Type | Visibility | Purpose |
|---|---|---|---|
| `profiles` | Table MultiSelect → `Profile Link` | visible | Pick one/many bundles. |
| `items_html` | HTML | `read_only` | Mount point for the grid (manual mode). |
| `items` | Table → `Item Link` | **`hidden` + `read_only`** | Effective items (derived or manual). |

```json
{ "fieldname": "profiles", "fieldtype": "Table MultiSelect", "options": "Profile Link" },
{ "fieldname": "items_html", "fieldtype": "HTML", "read_only": 1 },
{ "fieldname": "items", "fieldtype": "Table", "options": "Item Link", "hidden": 1, "read_only": 1 }
```

## Relationship summary

```
Item  ◀─ item ──  Item Link  ──┬── (in)  Profile.items
                               └── (in)  Consumer.items

Profile  ◀─ profile ──  Profile Link  ── (in) Consumer.profiles
```

Both `Profile.items` and `Consumer.items` use the **same** `Item Link` child —
remember this when wiring the widget: the `child_doctype` is `Item Link` in both
places, only the parent and (optionally) the field names differ.
