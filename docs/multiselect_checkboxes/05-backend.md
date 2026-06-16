# 05 · Backend — endpoint, expansion, guards

> Concern: **derivation & correctness**. The server is the source of truth; the
> JS in [04](04-frontend-binding.md) is a convenience layer over these methods.

## A. The grid data endpoint (`get_all_items`)

Feeds the checkbox grid. Filter out disabled (and any other non‑selectable)
items — the analog of core's `get_all_roles`.

```python
# myapp/.../doctype/profile/profile.py
import frappe
from frappe.model.document import Document


class Profile(Document):
    pass


@frappe.whitelist()
def get_all_items():
    """All selectable items for the checkbox grid."""
    return frappe.get_all(
        "Item",
        filters={"disabled": 0},
        pluck="name",
        order_by="name",
    )
```

> Point `ItemEditor`'s `data_method` option at this dotted path.

## B. The expansion helper (`populate_items_from_profiles`)

The heart of the pattern — the analog of `User.populate_role_profile_roles`.
Fully parameterized so any Consumer can reuse it (DRY). Keep it next to the
Profile doctype and import it from each Consumer.

```python
# myapp/.../doctype/profile/profile.py  (same module as above)
def populate_items_from_profiles(
    doc,
    profiles_field="profiles",     # Consumer's Table MultiSelect field
    items_field="items",           # Consumer's hidden items table
    profile_link_field="profile",  # Link field inside the Profile Link row
    item_link_field="item",        # Link field inside the Item Link row
):
    """Expand selected Profiles into the flat `items` table.

    Union the items of every selected profile; drop items no longer covered by
    any profile; append the new ones. No-op when no profile is selected, leaving
    manual selections intact. Idempotent: safe to run on every save.
    """
    profiles = doc.get(profiles_field)
    if not profiles:
        return

    new_items = set()
    for row in profiles:
        profile = frappe.get_cached_doc("Profile", row.get(profile_link_field))
        new_items.update(i.get(item_link_field) for i in profile.items)

    # keep still-valid rows, then append the missing ones
    kept = [i for i in doc.get(items_field) if i.get(item_link_field) in new_items]
    doc.set(items_field, kept)
    existing = {i.get(item_link_field) for i in kept}
    for item in new_items:
        if item not in existing:
            doc.append(items_field, {item_link_field: item})
```

Algorithm, line by line:

1. **No profiles → return** (manual mode is left untouched).
2. **Union** every profile's items into a `set` (dedups overlaps automatically).
3. **Prune** existing rows down to those still in the union (drops items from a
   removed profile).
4. **Append** any union members not already present.

Net result: in profile mode, `items` becomes *exactly* the union — derived, not
hand‑edited.

## C. Wire it into each Consumer

```python
# myapp/.../doctype/sales_order/sales_order.py
import frappe
from frappe.model.document import Document
from myapp.path.to.profile import populate_items_from_profiles


class SalesOrder(Document):
    def validate(self):
        self.populate_profile_items()

    @frappe.whitelist()
    def populate_profile_items(self):
        """Expand selected profiles into the items table."""
        populate_items_from_profiles(self)
```

Two call sites, by design:

- **`validate()`** — runs on every save. **Authoritative**: even if the UI is
  bypassed (API, data import), the items table is correct.
- **`@frappe.whitelist() populate_profile_items()`** — called from JS via
  `frm.call("populate_profile_items")` for instant feedback when a profile is
  added. A whitelisted **document method** is callable through `frm.call`.

> If a field name differs on a given Consumer, pass overrides:
> `populate_items_from_profiles(self, items_field="order_items")`.

## D. Junction dedup guard (recommended)

Already shown in [02](02-data-model.md#2-item-link--the-shared-junction-child):
`Item Link.before_insert` rejects a duplicate item within the same parent — a
DB‑level safety net beneath the JS dedup. Mirrors `Has Role`.

## E. Optional — cascade profile edits to consumers

When a **Profile** changes, existing consumers won't update until re‑saved. To
propagate (the analog of `Role Profile.update_all_users`):

```python
# profile.py
class Profile(Document):
    def on_update(self):
        self.queue_action(
            "update_consumers",
            now=frappe.in_test or frappe.flags.in_install,
            enqueue_after_commit=True,
            queue="long",
        )

    def update_consumers(self):
        # re-save every consumer that references this profile; validate() re-expands
        names = frappe.get_all("Profile Link", filters={"profile": self.name}, pluck="parent")
        for name in set(names):
            frappe.get_doc("<Consumer DocType>", name).save()
```

Note: it does **not** re‑implement expansion — it just re‑saves consumers and
lets the idempotent `validate()` recompute. Run it on the `long` queue and
`enqueue_after_commit` so the UI stays responsive. Skip this section if your
consumers should keep the profile snapshot they had at creation time. For
submittable consumers, guard against editing submitted docs (only re‑save
`docstatus == 0`).
