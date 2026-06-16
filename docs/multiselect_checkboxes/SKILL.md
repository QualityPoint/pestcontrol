---
name: frappe-multiselect-checkbox-editor
description: >-
  Implement a multi-select checkbox editor with reusable bundles ("profiles") in
  any custom Frappe/ERPNext app — the generalization of Frappe core's
  User/Role/Role Profile + RoleEditor design. Use this when a user wants to
  assign MANY of some atomic entity (roles, tags, pest types, skills,
  permissions, services…) to a document via a checkbox grid, AND/OR bundle those
  entities into named, reusable profiles that auto-expand onto a consumer
  document. Triggers: "checkbox grid for assigning X", "like how Frappe assigns
  roles / role profiles", "multi-select that expands a profile into items",
  "RoleEditor-style widget", "hidden child table synced from checkboxes".
---

# Frappe Multi‑Select Checkbox Editor (Profile → Items)

This skill teaches a complete, app‑agnostic pattern: a hidden read‑only child
table is the source of truth; an HTML field hosts a checkbox grid that syncs
into it; and a `Table MultiSelect` of profiles can derive that table as the
union of every profile's items. It is the generalized form of Frappe's
`RoleEditor` / `Role Profile` / `User` mechanism.

## When to apply

Apply when ALL hold:
- There is an **atomic, reusable entity** attached to documents (the *Item*).
- Users pick **several at once** — a checkbox grid beats a child‑table grid.
- Named **bundles** of items (the *Profile*) should be reusable across documents.
- A document (the *Consumer*) takes **one or many profiles** and has its item
  list **derived** from them, while still allowing manual selection when none.

Do NOT apply when a plain `Table MultiSelect` (no bundling, no checkbox grid)
already suffices — use that instead.

## How to use this skill

Read the layered docs in order; each covers ONE concern (kept short on purpose):

1. [README.md](README.md) — overview, terminology map (generic ↔ Frappe core ↔ target app), mental model.
2. [01-architecture.md](01-architecture.md) — the 5 actors, 3 layers, data flow, dual‑mode state machine.
3. [02-data-model.md](02-data-model.md) — the 5 doctypes and exact fields (note the `hidden` + `read_only` flags on the items table).
4. [03-frontend-editor.md](03-frontend-editor.md) — the `ItemEditor` checkbox widget (full code).
5. [04-frontend-binding.md](04-frontend-binding.md) — mounting on Profile & Consumer forms; the DRY one‑line binder.
6. [05-backend.md](05-backend.md) — `get_all_items` endpoint, `populate_items_from_profiles` expansion, validate hooks, dedup guard, optional cascade.
7. [06-implementation-checklist.md](06-implementation-checklist.md) — ordered steps, 10 gotchas, and a verification script.

## Workflow for the agent

1. **Map names first.** Fill the terminology table in the README with the
   target app's real names (app namespace, Item, Item Link, Profile, Profile
   Link, Consumer, and the three fields). Everything else follows.
2. **Build bottom‑up:** schema ([02]) → backend ([05]) → widget ([03]) →
   binding ([04]) — the order in [06].
3. **Stay DRY:** put the widget and the consumer binder in the app's
   `app_include_js` bundle once; each consumer's `.js` is a single
   `bind_profile_editor(...)` call.
4. **Server is authoritative:** always expand in `validate()`, not just via the
   JS `frm.call`.
5. **Finish with:** `bench build --app <app>`, `bench --site <site> migrate`,
   and a browser hard‑refresh.
6. **Verify** using the script in [06](06-implementation-checklist.md#how-to-verify-it-works)
   (manual mode, profile mode, server authority, dedup, disabled item).

## Canonical reference to consult

When in doubt, read the proven core implementation it generalizes:
- `frappe/core/doctype/user/user.py` → `populate_role_profile_roles`, `get_all_roles`
- `frappe/core/doctype/role_profile/role_profile.{py,js}`
- `frappe/public/js/frappe/roles_editor.js` → `frappe.RoleEditor`

[01-architecture.md]: 01-architecture.md
[02]: 02-data-model.md
[03]: 03-frontend-editor.md
[04]: 04-frontend-binding.md
[05]: 05-backend.md
[06]: 06-implementation-checklist.md
