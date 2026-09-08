# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

"""Tests for the language-prefix resolver.

These matter more than most. `website_path_resolver` replaces frappe's own
path resolution for *every* request, and frappe 16 short-circuits only `desk`
before the hooks -- there is no `endpoint == "app"` shortcut -- so /app, /api
and the customer portal all pass through resolve(). A regression here takes
down the desk, not just the website.

Route rules only evaluate when a request is bound (evaluate_dynamic_routes
checks frappe.local.request), so every case binds a real werkzeug request.
"""

import frappe
from frappe.tests.utils import FrappeTestCase
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request

from pestcontrol.pc_website.router import resolve


def _bind(path, query=""):
	full = "/" + path.lstrip("/") + (f"?{query}" if query else "")
	frappe.local.request = Request(EnvironBuilder(path=full).get_environ())
	frappe.local.form_dict = frappe._dict(
		{k: v for k, v in (p.split("=", 1) for p in query.split("&") if "=" in p)}
	)


class TestLanguageRouter(FrappeTestCase):
	def setUp(self):
		frappe.local.lang = "en"

	# -- paths that must never be touched ---------------------------------

	def test_framework_paths_pass_through_unchanged(self):
		"""A redirect here would break the desk and the API."""
		for path in ("app", "app/website-service", "api/method/ping",
		             "assets/pestcontrol/website/css/custom.css",
		             "files/example.png", "private/files/x.png", "login"):
			with self.subTest(path=path):
				_bind(path)
				try:
					resolve(path)          # must not raise Redirect
				except frappe.Redirect:
					self.fail(f"/{path} was redirected; the desk or API would break")
				self.assertEqual(frappe.local.pc_prefix, "")

	def test_machine_readable_paths_pass_through(self):
		for path in ("sitemap.xml", "robots.txt", "favicon.ico"):
			with self.subTest(path=path):
				_bind(path)
				try:
					resolve(path)
				except frappe.Redirect:
					self.fail(f"/{path} must not be language-prefixed")

	def test_portal_cluster_is_not_prefixed(self):
		"""Derived from the site's own website_route_rules, not hardcoded."""
		for path in ("orders", "invoices", "quotations", "addresses", "tasks"):
			with self.subTest(path=path):
				_bind(path)
				try:
					resolve(path)
				except frappe.Redirect:
					self.fail(f"/{path} is a portal route and must stay unprefixed")

	# -- the /project collision -------------------------------------------

	def test_bare_project_belongs_to_erpnext(self):
		"""erpnext claims /project for its portal list."""
		_bind("project")
		try:
			resolve("project")
		except frappe.Redirect:
			self.fail("/project is erpnext's portal list and must stay unprefixed")

	def test_project_detail_belongs_to_us(self):
		"""Website Project generates /project/<slug>, which we do prefix."""
		_bind("project/some-slug")
		with self.assertRaises(frappe.Redirect):
			resolve("project/some-slug")
		self.assertTrue(frappe.flags.redirect_location.startswith("/"))
		self.assertIn("/project/some-slug", frappe.flags.redirect_location)

	# -- redirects to the default language --------------------------------

	def test_root_redirects_to_default_language(self):
		_bind("")
		with self.assertRaises(frappe.Redirect):
			resolve("")
		self.assertEqual(frappe.flags.redirect_location, f"/{self._default()}/")

	def test_unprefixed_page_redirects(self):
		_bind("about")
		with self.assertRaises(frappe.Redirect):
			resolve("about")
		self.assertEqual(frappe.flags.redirect_location, f"/{self._default()}/about")

	def test_lang_query_param_picks_the_target_and_is_dropped(self):
		"""Migration shim for URLs the old cookie switcher left in the wild."""
		_bind("about", "_lang=en")
		with self.assertRaises(frappe.Redirect):
			resolve("about")
		self.assertEqual(frappe.flags.redirect_location, "/en/about")

	def test_other_query_params_survive_the_redirect(self):
		_bind("about", "utm_source=google")
		with self.assertRaises(frappe.Redirect):
			resolve("about")
		self.assertIn("utm_source=google", frappe.flags.redirect_location)

	# -- prefixed paths resolve ------------------------------------------

	def test_prefixed_root_is_the_marketing_home(self):
		"""Never the role/portal home, even for a logged-in user."""
		_bind("ar/")
		endpoint = resolve("ar/")
		self.assertEqual(endpoint, (frappe.get_hooks("home_page") or ["home"])[-1])
		self.assertEqual(frappe.local.lang, "ar")
		self.assertEqual(frappe.local.pc_prefix, "/ar")

	def test_prefix_sets_language_and_strips_itself(self):
		for lang in ("ar", "en"):
			with self.subTest(lang=lang):
				_bind(f"{lang}/about")
				endpoint = resolve(f"{lang}/about")
				self.assertEqual(endpoint, "about")
				self.assertEqual(frappe.local.lang, lang)
				self.assertEqual(frappe.local.pc_prefix, f"/{lang}")
				self.assertEqual(frappe.local.pc_bare_path, "about")

	def test_prefixed_generator_route_resolves(self):
		route = frappe.db.get_value("Website Service", {"published": 1}, "route")
		if not route:
			self.skipTest("no published Website Service on this site")
		_bind(f"ar/{route}")
		self.assertEqual(resolve(f"ar/{route}"), route)
		self.assertEqual(frappe.local.lang, "ar")

	def test_unknown_prefixed_path_is_not_redirected(self):
		"""It should 404 through the normal renderers, not bounce."""
		_bind("ar/does-not-exist")
		try:
			resolve("ar/does-not-exist")
		except frappe.Redirect:
			self.fail("a missing page under a prefix must 404, not redirect")

	def _default(self):
		langs = {r["code"] for r in frappe.get_all("Language", filters={"enabled": 1},
		                                           fields=["name as code"])}
		configured = frappe.db.get_single_value("PC Website Settings", "default_language")
		return configured if configured in langs else "en"
