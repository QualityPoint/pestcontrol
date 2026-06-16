# Multi‑Select Checkbox Editor — Pattern Guide

A reusable, app‑agnostic recipe for letting a user **assign many items via a
checkbox grid**, and **bundle those items into reusable profiles** that expand
automatically onto a consumer document.

This is a generalization of Frappe core's **User / Role / Role Profile** design
(`frappe.RoleEditor`). If you understand how a Role Profile expands into a
User's roles, you already understand this pattern.

> The docs below are intentionally split (separation of concerns). Read them in
> order, or jump to the layer you're working on. Each file is short and focused.

## When to use this pattern

Use it when **all** of the following hold:

- You have an **atomic, reusable entity** that gets attached to documents
  (the *Item* — e.g. Role, Pest Type, Tag, Permission, Skill).
- Users pick **several at once**; a checkbox grid beats a child‑table grid.
- You want **named bundles** of those items (the *Profile*) that can be reused
  across many documents and edited in one place.
- A document should be able to take **one or many profiles** and have its item
  list **derived** from them — while still allowing manual selection when no
  profile is attached.

If you only need a multi‑select with no bundling, use a plain
`Table MultiSelect` field and stop here — you don't need this pattern.

## Terminology (used consistently across all docs)

| Generic term (this guide) | Frappe core equivalent | Role in the pattern |
|---|---|---|
| **Item** | `Role` | Atomic assignable entity (standalone doctype) |
| **Item Link** | `Has Role` | Junction child row holding one Item |
| **Profile** | `Role Profile` | Named reusable bundle of Items |
| **Profile Link** | `User Role Profile` | Junction child row holding one Profile |
| **Consumer** | `User` | Document that selects Profiles and gets expanded Items |
| **ItemEditor** (JS) | `frappe.RoleEditor` | MultiCheck grid widget |
| `get_all_items` | `get_all_roles` | Endpoint feeding the grid |
| `populate_items_from_profiles` | `populate_role_profile_roles` | Profile → Item expansion |

Throughout the code samples the example app namespace is `myapp`. Replace
`myapp`, `Item`, `Profile`, etc. with your real names.

## Document index

> Using this as a Claude Code Skill? Start at [SKILL.md](SKILL.md) — it is the
> manifest (description + trigger conditions + agent workflow) that points back
> into the docs below.

| File | Concern |
|---|---|
| [01-architecture.md](01-architecture.md) | The actors, the layers, and the data flow |
| [02-data-model.md](02-data-model.md) | DocTypes & fields to create |
| [03-frontend-editor.md](03-frontend-editor.md) | The generic `ItemEditor` checkbox widget |
| [04-frontend-binding.md](04-frontend-binding.md) | Wiring the widget onto Profile & Consumer forms |
| [05-backend.md](05-backend.md) | Endpoint, expansion helper, guards, validate hooks |
| [06-implementation-checklist.md](06-implementation-checklist.md) | Ordered steps, gotchas, and how to verify |

## The one‑paragraph mental model

A **hidden, read‑only child table** (`items`) is the single source of truth for
what is assigned. The user never edits it directly. Instead, an **HTML field**
(`items_html`) hosts a checkbox grid that *syncs into* that table. On a
**Consumer**, a `Table MultiSelect` of **Profiles** can take over: when profiles
are attached, the item table is **derived** (union of every profile's items) and
the grid is **locked**; when no profile is attached, the grid is editable for
manual selection. Everything is **idempotent** and **server‑authoritative**.
