# 06 · Implementation checklist & gotchas

> A linear recipe to reproduce the pattern in any custom Frappe app, plus the
> traps to avoid. Use this as the verification pass.

## Ordered steps

**Schema** ([02](02-data-model.md))
1. [ ] Create **Item** (standalone): `item_name` (Data, reqd, unique), `disabled` (Check); `autoname: field:item_name`.
2. [ ] Create **Item Link** (`istable`): `item` (Link → Item). Add `before_insert` dedup.
3. [ ] Create **Profile** (standalone): `profile_name` (Data, reqd, unique), `items_html` (HTML, read_only), `items` (Table → Item Link, **hidden + read_only**).
4. [ ] Create **Profile Link** (`istable`): `profile` (Link → Profile).
5. [ ] On each **Consumer**: add `profiles` (Table MultiSelect → Profile Link), `items_html` (HTML, read_only), `items` (Table → Item Link, **hidden + read_only**).

**Backend** ([05](05-backend.md))
6. [ ] Add `get_all_items()` whitelisted endpoint in `profile.py`.
7. [ ] Add `populate_items_from_profiles(doc, ...)` helper in `profile.py`.
8. [ ] On each Consumer: `validate()` → `self.populate_profile_items()`, plus a whitelisted `populate_profile_items()`.

**Frontend** ([03](03-frontend-editor.md), [04](04-frontend-binding.md))
9. [ ] Add `ItemEditor` (`components/item_editor.js`) and `bind_profile_editor` (`components/profile_editor.js`) to the app bundle.
10. [ ] Register both in `*.bundle.js`; ensure `app_include_js` points to it in `hooks.py`.
11. [ ] Profile form `.js`: mount `ItemEditor` on `refresh`, sync on `validate`.
12. [ ] Each Consumer `.js`: a single `myapp.bind_profile_editor(<Parent>, "Profile Link", "Item Link")`.

**Build & apply**
13. [ ] `bench build --app myapp` (required after any bundle change).
14. [ ] `bench --site <site> migrate` (to apply new doctypes/fields).
15. [ ] Hard‑refresh the browser (bundle hash changes).

## Gotchas (each one bit a real implementation)

| # | Trap | Fix |
|---|---|---|
| 1 | `items` table not `hidden`/`read_only` | Set both — otherwise users edit it directly and bypass the grid. |
| 2 | `ItemEditor` args reversed | Signature is **`(wrapper, frm, disable, options)`**, not `(frm, wrapper)`. |
| 3 | Wrong `child_doctype` on a consumer | It is the **junction** (`Item Link`), not the Item itself. |
| 4 | Forgot `validate` sync | `on_change` alone misses edge cases; always flush in `validate`. |
| 5 | Editing duplicated per consumer | Lift logic into the bundle binder (DRY); each `.js` is one line. |
| 6 | Bundle change not visible | Run `bench build` **and** hard‑refresh; the hashed filename changes. |
| 7 | Submittable consumer editable after submit | Gate the editor on `frm.doc.docstatus !== 0`. |
| 8 | Child add/remove events not firing | Register on the **child doctype** with `<parentfield>_add` / `_remove`. |
| 9 | Stale `amended_from` after a doctype rename | Point it back at the doctype's own (new) name, then `migrate`. |
| 10 | Expansion not idempotent | The union approach is; never *append‑only* without pruning. |

## How to verify it works

- **Manual mode:** open a Consumer with no profile → tick a few items → save →
  reopen → the same items are checked and present in `items`.
- **Profile mode:** add a profile → grid locks, shows that profile's items →
  save → `items` equals the union. Add a second overlapping profile → no
  duplicates. Remove all profiles → grid editable again.
- **Server authority:** set `profiles` via API/console and `.save()` (no UI) →
  `items` is still the correct union (proves `validate` is authoritative).
- **Dedup guard:** try to append a duplicate `Item Link` in console → it throws.
- **Disabled item:** set an Item's `disabled = 1` → it disappears from the grid
  (`get_all_items` filters it).

## Naming map back to your app

When training on a concrete app, substitute the generic names:

| Generic | Your app fills in |
|---|---|
| `myapp` | app namespace |
| `Item` / `Item Link` | atomic entity + its junction |
| `Profile` / `Profile Link` | bundle + its junction |
| `Consumer` | each business doctype that assigns items |
| `items` / `items_html` / `profiles` | the three fields you add |
| `ItemEditor` / `bind_profile_editor` | widget + binder names |
