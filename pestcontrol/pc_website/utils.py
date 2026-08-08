# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import re

import frappe
from frappe import _


def get_website_context(context):
    """Common context every pestcontrol www/ page needs: current year,
    the site-wide settings singleton, and the active language."""
    context.year = frappe.utils.now_datetime().year
    settings = frappe.get_cached_doc("PC Website Settings").as_dict()
    attach_translations("PC Website Settings", [settings])
    context.settings = settings
    context.lang = frappe.local.lang


def attach_translations(doctype, items):
    """Batch-fetch Website Language rows for a list of already-fetched items
    and stash them on each item for localize() to read — one query per page,
    not one query per item."""
    if not items:
        return items

    rows = frappe.get_all(
        "Website-Language",
        filters={"parenttype": doctype, "parent": ["in", [item.name for item in items]]},
        fields=["parent", "language", "fieldname", "translated_value"],
    )
    by_parent = {}
    for row in rows:
        by_parent.setdefault(row.parent, {})[(row.language, row.fieldname)] = row.translated_value

    for item in items:
        item["_translations"] = by_parent.get(item.name, {})
    return items


def get_translated_list(doctype, **kwargs):
    """Drop-in replacement for frappe.get_all on a translatable doctype —
    same signature, with per-language translations batch-attached."""
    items = frappe.get_all(doctype, **kwargs)
    return attach_translations(doctype, items)


def localize(item, fieldname):
    """Return the translated value of `fieldname` for the active language,
    falling back to the default-language field when no translation exists."""
    lang = frappe.local.lang
    if lang and lang != "en":
        value = (item.get("_translations") or {}).get((lang, fieldname))
        if value:
            return value
    return item.get(fieldname)


def make_route(value):
    """Slugify `value` into a URL-safe route segment."""
    return re.sub(r"[^a-z0-9]+", "-", (value or "").lower()).strip("-")


def validate_translations(doc):
    """Raise if the `translations` child table has more than one row for the
    same (language, fieldname) pair — the last one would otherwise silently
    win with no indication why."""
    seen = set()
    for row in doc.get("translations") or []:
        key = (row.language, row.fieldname)
        if key in seen:
            frappe.throw(
                _("Duplicate translation for language {0}, field {1}").format(row.language, row.fieldname)
            )
        seen.add(key)
