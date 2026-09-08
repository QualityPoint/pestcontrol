# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

"""Overrides frappe's /sitemap.xml.

Frappe's own version (frappe/www/sitemap.py) emits a bare <loc>/<lastmod>
per URL with no hreflang alternates, which is no use on a bilingual site.
This keeps its two data sources -- www pages that opt in with `sitemap = 1`,
and published website-generator documents -- and adds the alternates.

The app's copy wins over frappe's because both the jinja loader and
TemplatePage.set_template_path walk `reversed(get_installed_apps())`, and
pestcontrol installs after frappe.
"""

from urllib.parse import quote

import frappe
from frappe.utils import get_url, nowdate
from frappe.website.router import get_pages
from frappe.website.utils import get_home_page
from frappe.www.sitemap import get_public_pages_from_doctypes

from pestcontrol.pc_website.utils import get_site_languages


no_cache = 1
base_template_path = "www/sitemap.xml"

# Real pages, but nothing a search engine should be indexing.
EXCLUDE = frozenset(("404", "account/login", "account/signup", "me", "portal",
                     "sitemap.xml", "robots.txt", "index"))


def get_context(context):
	home = get_home_page()
	entries = {}

	for route, page in get_pages().items():
		if not page.sitemap or route in EXCLUDE:
			continue
		# The home page answers on "/" but is routed as "home"; listing both
		# would advertise a duplicate of the site root.
		entries["" if route == home else route] = nowdate()

	for route, data in get_public_pages_from_doctypes().items():
		if route and route not in EXCLUDE:
			entries[route] = f"{data['modified']:%Y-%m-%d}"

	settings = frappe.get_cached_doc("PC Website Settings")
	base = (settings.get("canonical_base_url") or get_url()).rstrip("/")

	# Languages come from the enabled Language records, never a constant, so
	# enabling one adds its URLs and its alternates here with no code change.
	languages = [row["code"] for row in get_site_languages()]
	default = settings.get("default_language")

	links = []
	for path, lastmod in sorted(entries.items()):
		alternates = [{"lang": lang, "href": _abs(base, path, lang)} for lang in languages]
		if default in languages:
			alternates.append({"lang": "x-default", "href": _abs(base, path, default)})
		# One <url> per language, each carrying the full alternates set --
		# google requires the annotations to be reciprocal, so every version
		# has to list every version including itself.
		for lang in languages:
			links.append({
				"loc": _abs(base, path, lang),
				"lastmod": lastmod,
				"alternates": alternates,
			})
	return {"links": links}


def _abs(base, path, lang):
	segment = quote(path.encode("utf-8")) if path else ""
	prefix = f"/{lang}" if lang else ""
	return f"{base}{prefix}/{segment}" if segment else f"{base}{prefix}/"
