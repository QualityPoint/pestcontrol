# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import re

import frappe
from frappe import _

# Maps each translatable doctype's semantic fieldnames onto the generic
# title/subtitle/context slots on its `article` (Website Article) bundle rows.
# `title` is always the doctype's primary translatable field.
ARTICLE_FIELD_MAP = {
    "PC Website Settings": {"address": "title", "about_footer_text": "context"},
    "Website Service": {
        "service_name": "title",
        "short_description": "subtitle",
        "full_description": "context",
    },
    "Website Project": {
        "project_name": "title",
        "short_description": "subtitle",
        "full_description": "context",
    },
    "Website Team Member": {"designation": "title", "bio": "context"},
    "Website Testimonial": {"designation": "title", "testimonial_text": "context"},
    "Website Pricing Plan": {"plan_name": "title"},
    "Pricing Plan Feature": {"feature_text": "title"},
    "Website FAQ": {"question": "title", "answer": "context"},
    "Website Gallery Item": {"title": "title"},
    "Website Blog Post": {"title": "title", "blog_intro": "subtitle", "content": "context"},
}


def get_website_context(context):
    """Common context every pestcontrol www/ page needs: current year,
    the site-wide settings singleton, and the active language."""
    context.year = frappe.utils.now_datetime().year
    settings = frappe.get_cached_doc("PC Website Settings").as_dict()
    attach_articles("PC Website Settings", [settings])
    context.settings = settings
    context.lang = frappe.local.lang


def attach_articles(doctype, items):
    """Batch-fetch Website Article rows for a list of already-fetched items
    and stash them on each item for localize() to read — one query per page,
    not one query per item."""
    if not items:
        return items

    rows = frappe.get_all(
        "Website Article",
        filters={
            "parenttype": doctype,
            "parentfield": "article",
            "parent": ["in", [item.name for item in items]],
        },
        fields=["parent", "language", "title", "subtitle", "context"],
    )
    by_parent = {}
    for row in rows:
        by_parent.setdefault(row.parent, {})[row.language] = {
            "title": row.title,
            "subtitle": row.subtitle,
            "context": row.context,
        }

    for item in items:
        # attribute assignment, not bracket assignment: `item` may be a real
        # Document (generator pages), which has no __setitem__, or a frappe
        # `_dict` (list pages), where attribute and bracket access are the
        # same thing anyway
        item.doctype = doctype
        item._articles = by_parent.get(item.name, {})
    return items


def get_translated_list(doctype, **kwargs):
    """Drop-in replacement for frappe.get_all on a translatable doctype —
    same signature, with per-language article bundles batch-attached."""
    items = frappe.get_all(doctype, **kwargs)
    return attach_articles(doctype, items)


def localize(item, fieldname):
    """Return the value of `fieldname` for the active language by looking up
    the matching slot on the item's `article` bundle, falling back to the
    English article when the current language's row is missing or has that
    particular field left blank (a partial translation)."""
    slot = ARTICLE_FIELD_MAP.get(item.get("doctype"), {}).get(fieldname)
    if not slot:
        return item.get(fieldname)

    articles = item.get("_articles") or {}
    lang = frappe.local.lang or "en"
    value = (articles.get(lang) or {}).get(slot)
    if value:
        return value
    return (articles.get("en") or {}).get(slot)


def route_from_article(doc):
    """Return the English article row's title, used to auto-slug `route`."""
    for row in doc.get("article") or []:
        if row.language == "en" and row.title:
            return row.title
    return None


def make_route(value):
    """Slugify `value` into a URL-safe route segment."""
    return re.sub(r"[^a-z0-9]+", "-", (value or "").lower()).strip("-")


def validate_articles(doc):
    """Raise if the `article` child table has more than one row for the same
    language — a bundle row *is* the whole translation, so a duplicate
    language would otherwise silently win with no indication why."""
    seen = set()
    for row in doc.get("article") or []:
        if row.language in seen:
            frappe.throw(_("Duplicate article for language {0}").format(row.language))
        seen.add(row.language)
