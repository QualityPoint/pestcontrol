# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

"""Search-engine metadata for the public website.

This fills the gaps in frappe's own metadata pipeline rather than replacing
it. `MetaTags` (frappe/website/website_components/metatags.py) already turns
`context.title`, `context.description` and `context.image` into the matching
`og:*` and `twitter:*` tags and renders them through
templates/includes/meta_block.html. What it does not produce -- canonical,
`og:url`, `og:site_name`, `og:locale`, `robots` -- is added here.

Registered as the `update_website_context` hook, which frappe runs for both
www pages (TemplatePage) and generator documents (DocumentPage), *after* the
page's own get_context(). That ordering is the reason this lives in a hook:
it needs to see `context.doc` and `context.title`, which do not exist yet
when get_website_context() runs as the first line of every get_context().
"""

import frappe
from frappe.utils import get_url, strip_html
from frappe.website.utils import get_home_page

from pestcontrol.pc_website.utils import article_value, localize

# First path segment that is not a public marketing page. The desk, the API
# and the customer portal must never get marketing metadata, and the
# machine-readable files must not get any at all.
SKIP_PREFIXES = frozenset((
	"app", "api", "assets", "files", "private", "backups", "socketio", "printview",
	"login", "update-password", "third_party",
	"portal", "me", "orders", "quotations", "invoices", "addresses", "shipments",
))
SKIP_EXACT = frozenset(("sitemap.xml", "robots.txt", "favicon.ico", "website_script.js"))

# Where to look for a share image on a generator document, best first.
DOC_IMAGE_FIELDS = ("header_image", "image", "cover_image", "photo", "icon")

# Doctype -> the fieldname holding its one-line summary. These are semantic
# names, so they resolve through localize()/ARTICLE_FIELD_MAP. Every one of
# them is already written and already per-language; it is simply never been
# emitted as a meta description before.
DOC_DESCRIPTION_FIELDS = {
	"Website Service": "short_description",
	"Website Project": "short_description",
	"Website Blog Post": "blog_intro",
	"Website Pest": "short_description",
	"Website Team Member": "bio",
}

DESCRIPTION_LIMIT = 155


def build_seo_context(context):
	"""`update_website_context` hook."""
	# `route` is the one key set for both page types. `path` is populated only
	# for www pages -- on a generator document it is still None at this point,
	# because frappe fills it in set_missing_values(), which runs after this
	# hook. Reading `path` alone silently canonicalised every generator page
	# to the site root.
	path = (context.get("route") or context.get("path") or "").strip("/")
	if path in SKIP_EXACT or path.split("/", 1)[0].lower() in SKIP_PREFIXES:
		return
	if not context.get("settings"):
		# The page never called get_website_context(), so it is not one of
		# ours -- a frappe or erpnext page rendering through the same hook.
		return

	settings = context.settings
	doc = context.get("doc")

	canonical = _canonical(settings, path)
	context.seo_canonical = canonical
	context.seo_alternates = []  # populated in the language-URL phase

	tags = context.setdefault("metatags", frappe._dict())

	# The og:/twitter: mirrors are written out by hand rather than left to
	# frappe. MetaTags derives them from title/description/image, but it runs
	# *before* this hook (base_template_page.post_process_context), so
	# anything set here would land in <meta name="..."> with no matching
	# og:/twitter: tag -- and an admin-authored meta_title would update
	# <title> while og:title silently kept the old one.
	explicit_title = _article_field(doc, context, "meta_title")
	if title := (explicit_title or context.get("title")):
		context.title = title
		tags["title"] = tags["og:title"] = tags["twitter:title"] = title
		# <title> normally gets the brand appended for the SERP, but an
		# admin-written meta_title is taken as the finished string -- they
		# have already decided the wording, and appending to it produces the
		# double-separator, over-length titles google truncates.
		context.seo_page_title = title if explicit_title else _with_brand(title, settings)

	if description := _description(doc, context, settings):
		tags["description"] = description
		tags["og:description"] = tags["twitter:description"] = description

	if image := _image(doc, settings):
		tags["image"] = tags["og:image"] = tags["twitter:image"] = image
		tags["twitter:card"] = "summary_large_image"

	tags["og:type"] = "article" if doc else "website"
	tags["og:url"] = canonical
	if site_name := settings.get("site_name"):
		tags["og:site_name"] = site_name
	if locale := _locale():
		tags["og:locale"] = locale
	if handle := settings.get("twitter_handle"):
		tags["twitter:site"] = handle
	tags["robots"] = _robots(context)


def _with_brand(title, settings):
	site_name = settings.get("site_name")
	if not site_name or title.endswith(site_name):
		return title
	return f"{title} | {site_name}"


def _article_field(doc, context, field):
	"""Admin-authored SEO value for the active language, from the Website
	Article child table. Falls back to the site-wide defaults held on PC
	Website Settings' own article rows."""
	if doc and (value := article_value(doc, field)):
		return value
	return article_value(context.settings, field)


def _description(doc, context, settings):
	"""Meta description, admin's value first.

	The fallbacks matter because they are already written: `subtitle` holds a
	one-line summary, per language, for services, projects, blog posts and
	pests -- it has simply never been emitted as a tag.
	"""
	if value := _article_field(doc, context, "meta_description"):
		return _clamp(value)
	if value := context.get("description"):
		return _clamp(value)
	if doc:
		if field := DOC_DESCRIPTION_FIELDS.get(doc.get("doctype")):
			if value := localize(doc, field):
				return _clamp(value)
		if value := article_value(doc, "context"):
			return _clamp(value)
	return _clamp(article_value(settings, "context"))


def _clamp(text, limit=DESCRIPTION_LIMIT):
	"""Collapse to a single line and truncate on a word boundary.

	Word boundary rather than a hard cut because these fields are Small Text
	and Text Editor: they carry newlines and pasted markup, and slicing an
	Arabic word mid-character breaks the letter-joining in the search result.
	"""
	text = " ".join(strip_html(text or "").split())
	if len(text) <= limit:
		return text
	return text[:limit].rsplit(" ", 1)[0].rstrip(" -,.،") + "…"


def _image(doc, settings):
	"""Absolute URL of the share image, admin's choice first."""
	image = None
	if doc:
		image = article_value(doc, "og_image") or next(
			(doc.get(f) for f in DOC_IMAGE_FIELDS if doc.get(f)), None
		)
	image = image or article_value(settings, "og_image") or settings.get("default_og_image")
	return get_url(image) if image else None


def _canonical(settings, path):
	"""One absolute URL per page, so query strings and any future language
	prefix cannot fragment it into duplicates.

	Built here rather than read from `context.canonical`: frappe sets that in
	set_missing_values(), which runs *after* this hook, so it is neither
	readable nor writable from here.
	"""
	base = (settings.get("canonical_base_url") or get_url()).rstrip("/")
	if path == get_home_page():
		# The home page is reachable as "/" but resolves to the endpoint named
		# by the home_page setting ("home"), which is what lands in
		# context.path. Canonicalising to /home would point the homepage at a
		# duplicate of itself -- the exact thing canonical exists to prevent.
		path = ""
	return f"{base}/{path}" if path else f"{base}/"


def _locale():
	"""og:locale from the active Language record.

	Derived, never mapped: a {"ar": "ar_SA"} lookup would need a new entry
	for every language the business adds.
	"""
	lang = frappe.local.lang or "en"
	return lang.replace("-", "_")


def _robots(context):
	if context.get("seo_noindex"):
		return "noindex, nofollow"
	return "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
