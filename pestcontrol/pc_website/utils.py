# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

import os
import re

import frappe
from frappe import _


def get_site_languages():
	"""Languages offered by the topbar switcher, sourced from the core
	Language doctype's `enabled` flag — enabling/disabling a language for
	the site is a desk action, not a code change. A language having no
	`Website Article`/translations yet just means it silently falls back to
	English, same as any other partial translation."""
	return frappe.get_all(
		"Language", filters={"enabled": 1}, fields=["name as code", "language_name as label"]
	)


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
	"Website FAQ": {"question": "title", "answer": "context"},
	"Website Gallery Item": {"title": "title"},
	"Website Blog Post": {"title": "title", "blog_intro": "subtitle", "content": "context"},
	"Website Pest": {"pest_name": "title", "short_description": "subtitle", "description": "context"},
	"Website Hero Slide": {"heading": "title", "kicker": "subtitle", "description": "context"},
	"Website Feature": {"title": "title", "description": "context"},
	"Website List Item": {"title": "title"},
}


def get_website_context(context):
	"""Common context every pestcontrol www/ page needs: current year,
	the site-wide settings singleton, and the active language."""
	languages = get_site_languages()
	apply_preferred_language_cookie(languages)
	context.year = frappe.utils.now_datetime().year
	# Our pages are standalone (never extend Frappe's own base template), so
	# `window.frappe`/`frappe.csrf_token` never exists client-side. Forms that
	# POST need the token rendered in directly. Only do this for real logged-in
	# sessions — Guest uses one shared session (sid=Guest) across all visitors,
	# so generating/reading a token there would leak between concurrent guests;
	# Guest POSTs already work because Frappe skips CSRF when there's no saved
	# session token at all, which stays true as long as we don't touch it here.
	context.csrf_token = frappe.local.session.data.csrf_token if frappe.session.user != "Guest" else ""
	context.is_logged_in = frappe.session.user != "Guest"
	# session.data.full_name isn't reliably populated depending on how the
	# session was created (e.g. straight through /api/method/login) — look
	# it up directly from the User doc instead, which is always accurate.
	context.user_full_name = frappe.utils.get_fullname() if context.is_logged_in else ""
	context.user_image_url = ""
	context.user_initials = ""
	if context.is_logged_in:
		context.user_image_url = frappe.db.get_value("User", frappe.session.user, "user_image") or ""
		if not context.user_image_url:
			name_parts = (context.user_full_name or frappe.session.user).split()
			context.user_initials = "".join(part[0] for part in name_parts[:2]).upper()
	settings = frappe.get_cached_doc("PC Website Settings").as_dict()
	attach_articles("PC Website Settings", [settings])
	context.settings = settings
	context.hero_slides = get_translated_list(
		"Website Hero Slide", filters={"published": 1}, fields="*", order_by="display_order asc"
	)
	context.lang = frappe.local.lang
	context.languages = languages
	context.current_language = next(
		(l for l in languages if l["code"] == context.lang),
		(languages[0] if languages else {"code": "en", "label": "English"}),
	)


def apply_preferred_language_cookie(languages):
	"""Frappe's own language resolution only honors the `preferred_language`
	cookie for Guest visitors — a logged-in user (e.g. an admin testing the
	site in the same browser as the desk) falls back to their profile
	language instead, silently dropping the switcher's choice on every
	navigation that doesn't explicitly carry ?_lang. Override that here so
	the cookie sticks site-wide, regardless of session state, matching what
	a public marketing site visitor expects.

	Also applied globally via the before_request hook (see
	apply_preferred_language_cookie_on_request) so it reaches the dashboard
	pages too — those don't call get_website_context() themselves, and for
	/orders, /quotations, /invoices specifically, ListPage hardcodes
	get_context() resolution to frappe's own www/portal.py regardless of
	pestcontrol's override (frappe/website/page_renderers/template_page.py's
	set_standard_path forces self.app = "frappe"), so a per-page call in
	pestcontrol's own www/portal.py wouldn't even reach those routes."""
	if frappe.form_dict.get("_lang"):
		return  # explicit request always wins; core already applied it
	cookie_lang = frappe.request.cookies.get("preferred_language")
	valid_codes = {l["code"] for l in languages}
	if cookie_lang and cookie_lang in valid_codes:
		frappe.local.lang = cookie_lang


def apply_preferred_language_cookie_on_request():
	"""before_request hook. Runs after frappe's own init_request() has
	already set frappe.local.lang from the session/user (see
	frappe.auth.HTTPRequest.set_lang) but before any page's get_context() or
	template render — so overriding it here reaches every route uniformly,
	regardless of which app's controller/template ends up handling the
	request. See apply_preferred_language_cookie for why this can't just
	live in each page's own get_context() instead."""
	apply_preferred_language_cookie(get_site_languages())


def asset_version(path):
	"""Cache-busting query value for a public/ asset, based on its mtime, so
	edits to CSS/JS show up immediately instead of waiting out the browser's
	long max-age on static assets."""
	full_path = frappe.get_app_path("pestcontrol", "public", path)
	try:
		return int(os.path.getmtime(full_path))
	except OSError:
		return 0


def current_lang():
	"""frappe.local.lang, exposed as a jinja method for the dashboard page
	overrides (portal.html/order.html/me.html) — there is no reliable bare
	`lang` global for normal www-page rendering (only a `frappe.lang`
	nested under a *different*, restricted jinja globals set used
	elsewhere); is_rtl() works because it's registered as a real global
	function via frappe/hooks.py, so this mirrors that instead of
	depending on an undefined bare `lang`."""
	return frappe.local.lang


def portal_user_info():
	"""Full name/email/avatar for the logged-in session user — used by the
	dashboard header (avatar shortcut) on the portal.html and order.html
	overrides, which don't otherwise carry a `current_user`-like context
	var the way frappe/www/me.py does."""
	return frappe.db.get_value(
		"User", frappe.session.user, ["full_name", "email", "user_image"], as_dict=True
	)


def doc_to_json(doc):
	"""Serialize a Document for embedding in a <script type="application/json">
	block — used by the portal detail-page override so the customer
	dashboard's React island renders from the same already permission-
	checked document the page itself computed, instead of a second
	client-side fetch."""
	return frappe.as_json(doc.as_dict())


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


def filter_by_language(rows):
	"""Given a flat list of rows each carrying a `language` field (e.g.
	Pricing Plan Feature, which stores one row per language directly rather
	than nesting a Website Article bundle — nested tables inside a child
	table are unreliable in both the desk grid and Document.append()),
	return the subset matching the active language, falling back to English
	when the active language has no rows at all."""
	lang = frappe.local.lang or "en"
	matches = [r for r in rows if r.get("language") == lang]
	if matches:
		return matches
	return [r for r in rows if r.get("language") == "en"]


def route_from_article(doc):
	"""Return the English article row's title, used to auto-slug `route`."""
	for row in doc.get("article") or []:
		if row.language == "en" and row.title:
			return row.title
	return None


def make_route(value):
	"""Slugify `value` into a URL-safe route segment."""
	return re.sub(r"[^a-z0-9]+", "-", (value or "").lower()).strip("-")


def validate_unique_language(doc, fieldname="article"):
	"""Raise if `fieldname`'s child table has more than one row for the same
	language — a row *is* the whole translation for that language, so a
	duplicate would otherwise silently win with no indication why."""
	seen = set()
	for row in doc.get(fieldname) or []:
		if row.language in seen:
			frappe.throw(_("Duplicate {0} for language {1}").format(fieldname, row.language))
		seen.add(row.language)


def validate_articles(doc):
	validate_unique_language(doc, "article")


def sync_portal_user_on_login():
	"""Ensure the logged-in Website User is listed in their Customer's Portal
	User table, so the customer portal and the pestcontrol dashboard actually
	show their own documents.

	ERPNext's own on_session_creation hook (create_customer_or_supplier)
	creates the Customer + Contact link on a self-registered customer's
	first login, but never populates Portal User itself — and Portal User is
	what get_transaction_list's customer-scoping filter actually reads
	(erpnext.controllers.website_list_for_contact.get_parents_for_user).
	Without this, a self-registered customer's portal (Orders/Quotations/
	Invoices) stays empty even though their documents genuinely exist and are
	correctly linked to them."""
	user = frappe.session.user
	if frappe.db.get_value("User", user, "user_type") != "Website User":
		return

	contact_name = frappe.db.get_value("Contact", {"email_id": user})
	if not contact_name:
		return

	customer = frappe.db.get_value(
		"Dynamic Link",
		{"parenttype": "Contact", "parent": contact_name, "link_doctype": "Customer"},
		"link_name",
	)
	if not customer:
		return

	if frappe.db.exists("Portal User", {"parenttype": "Customer", "parent": customer, "user": user}):
		return

	customer_doc = frappe.get_doc("Customer", customer)
	customer_doc.append("portal_users", {"user": user})
	customer_doc.save(ignore_permissions=True)


def get_language_row(rows):
	"""Given a list of rows each carrying a `language` field (one row per
	language, no nested bundle), return the row for the active language,
	falling back to English, then the first row available."""
	lang = frappe.local.lang or "en"
	by_lang = {r.get("language"): r for r in rows}
	return by_lang.get(lang) or by_lang.get("en") or (rows[0] if rows else None)
