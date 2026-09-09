# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

"""Tests for self-registration.

The bug this endpoint replaces is worth restating, because the tests are
shaped around it: frappe's own sign_up() sets a random password and depends on
a verification email to let the user choose one. This site has no outgoing
Email Account, so every account it created was enabled but impossible to log
into. So the assertion that matters most here is not "a User row exists" -- it
is that the chosen password actually authenticates.
"""

from urllib.parse import urlparse

import frappe
from frappe.tests.utils import FrappeTestCase, change_settings
from frappe.utils.password import check_password
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request

from pestcontrol.pc_website.api import register_account

EMAIL = "_test_signup@example.com"
PASSWORD = "correct-horse-battery-7"


def _cleanup():
	if frappe.db.exists("User", EMAIL):
		frappe.delete_doc("User", EMAIL, force=True, ignore_permissions=True)


def _bind_request(path="/account/signup"):
	frappe.local.request = Request(EnvironBuilder(path=path).get_environ())
	# The endpoint is rate limited per IP, and the limiter reads request_ip
	# directly rather than deriving it from the request object.
	frappe.local.request_ip = "127.0.0.1"
	frappe.cache.delete_keys("rl:")


def _register(**overrides):
	args = {
		"full_name": "Test Signup",
		"email": EMAIL,
		"mobile_no": "+966500000000",
		"password": PASSWORD,
	}
	args.update(overrides)
	# The endpoint is whitelisted for Guest, which is who really calls it.
	frappe.set_user("Guest")
	try:
		return register_account(**args)
	finally:
		frappe.set_user("Administrator")


class TestRegisterAccount(FrappeTestCase):
	def setUp(self):
		super().setUp()
		frappe.set_user("Administrator")
		_cleanup()

	def tearDown(self):
		frappe.set_user("Administrator")
		_cleanup()
		if hasattr(frappe.local, "request"):
			del frappe.local.request
		super().tearDown()

	# --- the account is actually usable -----------------------------------

	def test_the_chosen_password_authenticates(self):
		"""The whole point: frappe's sign_up left an account nobody could enter."""
		_register()
		self.assertEqual(check_password(EMAIL, PASSWORD), EMAIL)

	def test_account_is_enabled_without_admin_approval(self):
		_register()
		user = frappe.get_doc("User", EMAIL)
		self.assertTrue(user.enabled)
		self.assertEqual(user.user_type, "Website User")
		self.assertEqual(user.mobile_no, "+966500000000")

	def test_gets_the_portal_default_role(self):
		"""Customer here -- what erpnext keys the Customer/Contact creation off."""
		_register()
		default_role = frappe.get_single_value("Portal Settings", "default_role")
		self.assertIn(default_role, frappe.get_roles(EMAIL))

	def test_returns_a_redirect_target(self):
		result = _register()
		self.assertTrue(result["success"])
		self.assertFalse(result["verify"])
		self.assertEqual(result["redirect_to"], "/portal")

	# frappe's sanitize_redirect compares the target against the current
	# request's host, so these two only mean anything with a request bound.
	# It always returns an absolute URL on our own host, never a bare path.
	def test_honours_a_safe_redirect(self):
		_bind_request()
		target = urlparse(_register(redirect_to="/orders")["redirect_to"])
		self.assertEqual(target.path, "/orders")
		self.assertEqual(target.netloc, "localhost")

	def test_rejects_an_offsite_redirect(self):
		"""The property that matters: a signup link cannot hand the newly
		logged-in visitor to somebody else's host."""
		_bind_request()
		target = urlparse(_register(redirect_to="https://evil.example.com/phish")["redirect_to"])
		self.assertEqual(target.netloc, "localhost")
		self.assertNotIn("phish", target.path)

	# --- weak passwords ----------------------------------------------------

	def test_rejects_a_weak_password(self):
		"""System Settings.enable_password_policy is 0 on this site, so frappe's
		own check passes everything -- this endpoint applies its own floor."""
		with self.assertRaises(frappe.ValidationError):
			_register(password="123456")
		self.assertFalse(frappe.db.exists("User", EMAIL))

	def test_rejects_a_short_password(self):
		with self.assertRaises(frappe.ValidationError):
			_register(password="Ab1!x")
		self.assertFalse(frappe.db.exists("User", EMAIL))

	def test_rejects_a_password_built_from_the_users_own_details(self):
		with self.assertRaises(frappe.ValidationError):
			_register(password="Test Signup 1")
		self.assertFalse(frappe.db.exists("User", EMAIL))

	# --- bad input ---------------------------------------------------------

	def test_rejects_a_malformed_email(self):
		with self.assertRaises(frappe.ValidationError):
			_register(email="not-an-email")

	def test_rejects_missing_fields(self):
		with self.assertRaises(frappe.ValidationError):
			_register(mobile_no="")

	def test_duplicate_returns_a_message_rather_than_throwing(self):
		"""The form shows this inline; an exception would read as a server error."""
		_register()
		result = _register()
		self.assertFalse(result["success"])
		self.assertIn("Registered", result["message"])

	def test_email_is_normalised(self):
		_register(email="  _TEST_SIGNUP@Example.com  ")
		self.assertTrue(frappe.db.exists("User", EMAIL))


class TestEmailVerification(FrappeTestCase):
	"""The verification branch, which is off by default on this site.

	It is tested anyway because the failure it guards against is the same one
	frappe's sign_up() has: an account created but never activatable. A branch
	that is dormant today is exactly the kind that ships broken.
	"""

	def setUp(self):
		super().setUp()
		frappe.set_user("Administrator")
		_cleanup()
		# frappe's own context manager rather than set_single_value: the latter
		# leaves the singles cache holding the test's value after the class
		# rolls back, which then leaks into every other test in the module.
		# commit=True because verify_account() commits (it has to -- see the
		# comment there), which would otherwise flush this test's setting
		# change into the real site and leak it into every later test.
		self._settings = change_settings("PC Website Settings", require_email_verification=1, commit=True)
		self._settings.__enter__()

	def tearDown(self):
		self._settings.__exit__(None, None, None)
		_cleanup()
		if hasattr(frappe.local, "request"):
			del frappe.local.request
		super().tearDown()

	def test_refuses_to_sign_up_when_the_site_cannot_send_email(self):
		"""Better to refuse than to strand an account nobody can activate.

		This site has no outgoing Email Account, which is exactly why the
		setting ships off.
		"""
		self.assertFalse(frappe.db.exists("Email Account", {"enable_outgoing": 1}))
		with self.assertRaises(frappe.ValidationError):
			_register()
		self.assertFalse(frappe.db.exists("User", EMAIL))

	def test_a_pending_account_starts_disabled_and_the_link_enables_it(self):
		"""Drives the verify endpoint directly, since no mail can be sent here."""
		from frappe.utils import cint, now_datetime
		from frappe.utils.verified_command import get_signed_params

		from pestcontrol.pc_website.api import VERIFICATION_TTL, verify_account

		user = frappe.get_doc(
			{
				"doctype": "User",
				"email": EMAIL,
				"first_name": "Pending",
				"user_type": "Website User",
				"enabled": 0,
				"new_password": PASSWORD,
				"send_welcome_email": 0,
			}
		)
		user.flags.ignore_permissions = True
		user.insert()
		self.assertEqual(frappe.db.get_value("User", EMAIL, "enabled"), 0)

		expires = cint(now_datetime().timestamp()) + VERIFICATION_TTL
		params = get_signed_params({"email": EMAIL, "expires": expires})
		_bind_request(f"/api/method/verify_account?{params}")
		frappe.local.flags.signed_query_string = params

		# The real caller is a query string, so this arrives as text.
		with self.assertRaises(frappe.Redirect):
			verify_account(email=EMAIL, expires=str(expires))
		self.assertEqual(frappe.db.get_value("User", EMAIL, "enabled"), 1)

	def test_an_unsigned_link_does_not_enable_anything(self):
		"""Without the HMAC, guessing an email address would be enough."""
		from pestcontrol.pc_website.api import verify_account

		user = frappe.get_doc(
			{
				"doctype": "User",
				"email": EMAIL,
				"first_name": "Pending",
				"user_type": "Website User",
				"enabled": 0,
				"new_password": PASSWORD,
				"send_welcome_email": 0,
			}
		)
		user.flags.ignore_permissions = True
		user.insert()

		params = f"email={EMAIL}&expires=99999999999"
		_bind_request(f"/api/method/verify_account?{params}")
		frappe.local.flags.signed_query_string = params

		verify_account(email=EMAIL, expires="99999999999")
		self.assertEqual(frappe.db.get_value("User", EMAIL, "enabled"), 0)
