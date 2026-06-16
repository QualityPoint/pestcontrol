# 01 · Architecture

> Prerequisite vocabulary: [README · Terminology](README.md#terminology-used-consistently-across-all-docs)

## The five actors

```
            ┌─────────────┐  bundles many   ┌──────────────┐
            │   Profile   │ ──────────────▶ │  Item Link   │ ── item ──▶ ┌──────┐
            │ (bundle of  │   (its hidden   │  (junction)  │             │ Item │
            │   items)    │    items table) └──────────────┘             └──────┘
            └─────────────┘                                                  ▲
                  ▲                                                          │
                  │ referenced by                                  item ─────┘
            ┌──────────────┐                                  ┌──────────────┐
            │ Profile Link │ ◀── selects many ── Consumer ──▶ │  Item Link   │
            │  (junction)  │     (profiles field)  expands to │  (junction)  │
            └──────────────┘                     (items table)└──────────────┘
```

- **Item** — the atomic thing being assigned. Standalone doctype with a
  `disabled` flag so retired items disappear from the grid.
- **Item Link** — a child (`istable`) with a single `Link → Item` field. It is
  the *junction* used by **both** Profile and Consumer to store items. Reusing
  one junction type is what makes Profile→Consumer expansion a trivial copy.
- **Profile** — a named, reusable bundle. Holds its own hidden `items` table
  (of Item Link rows).
- **Profile Link** — a child (`istable`) with a single `Link → Profile` field;
  the junction the Consumer uses to select profiles.
- **Consumer** — any document that assigns items. Has a `profiles`
  `Table MultiSelect` *and* its own hidden `items` table.

## The three layers (separation of concerns)

| Layer | Responsibility | Lives in |
|---|---|---|
| **Storage** | The hidden, read‑only `items` child table — the source of truth | DocType schema ([02](02-data-model.md)) |
| **Editing UI** | Checkbox grid that syncs into the storage table | `ItemEditor` widget ([03](03-frontend-editor.md)) |
| **Derivation** | Expand selected profiles → items; keep everything consistent | Backend helpers ([05](05-backend.md)) |

The golden rule: **nothing edits `items` directly by hand.** It is always
*derived* — either from the checkbox grid (manual mode) or from the attached
profiles (profile mode).

## Data flow

**Manual mode** (no profiles attached, or on the Profile form itself):

```
user ticks checkbox ─▶ ItemEditor.set_values_in_table()
                       ─▶ add/remove rows in hidden `items` table
                       ─▶ on save, server stores `items` as‑is
```

**Profile mode** (Consumer has ≥1 profile):

```
user adds a Profile Link ─▶ JS locks the grid (disable = 1)
                          ─▶ frm.call(populate endpoint)
server: populate_items_from_profiles()
        ─▶ items = UNION of every attached profile's items
        ─▶ grid re‑renders: derived items shown, checkboxes disabled
on save ─▶ server validate() recomputes the union (authoritative)
```

## Dual‑mode state machine (Consumer only)

| Condition | Grid state | `items` source of truth |
|---|---|---|
| `profiles` is empty | **editable** | the checkbox grid (manual) |
| `profiles` has ≥1 row | **locked** (disabled, checked) | union of profiles' items |
| document is submitted (`docstatus != 0`) | **not mounted** | frozen |

The Profile form has no dual mode — it only ever uses **manual mode** (it *is*
the bundle being authored).

## Why this design holds up

1. **Single source of truth** (`items`) that is never hand‑edited — only synced.
2. **Idempotent derivation** — the union recomputes to the same result on every
   save, so re‑running it (e.g. after a profile changes) is always safe.
3. **One shared junction** (`Item Link`) → expansion is a structural copy, not a
   transform.
4. **Server‑authoritative** — the JS sync is a convenience; `validate()` has the
   final word, so the data is correct even if the UI is bypassed.
5. **Reusable widget** — the same grid drives the Profile form and every
   Consumer, configured by a small options object.
