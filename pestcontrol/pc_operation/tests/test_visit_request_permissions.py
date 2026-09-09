# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

"""Tests for portal-customer access to Visit Request.

The failure this guards against is not subtle: the Customer role holds a
direct DocPerm on Visit Request, and every self-registered website user is
given that role, so before these hooks existed any registered visitor could
read every customer's visit requests through /api/resource/Visit Request.

Each test therefore asserts against a *second* customer's record -- the whole
point is what a portal user cannot reach, not what they can.
"""

import frappe
from frappe.tests.utils import FrappeTestCase

from pestcontrol.pc_operation.permissions import (
	visit_request_has_permission,
	visit_request_query,
)

COMPANY = "Sky Star"
CUSTOMER_A = "_Test Portal Customer A"
CUSTOMER_B = "_Test Portal Customer B"
USER_A = "_test_portal_a@example.com"
USER_B = "_test_portal_b@example.com"
USER_UNLINKED = "_test_portal_unlinked@example.com"


def _customer(name):
	if not frappe.db.exists("Customer", name):
		frappe.get_doc({"doctype": "Customer", "customer_name": name, "customer_type": "Individual"}).insert(
			ignore_permissions=True
		)
	return name


def _portal_user(email, customer=None):
	"""A Website User with the Customer role, optionally linked to a Customer.

	The Portal User child row is what erpnext's get_parents_for_user() reads,
	and it is the only thing that makes a customer's records visible -- so the
	unlinked case is a real state a freshly registered user passes through.
	"""
	if not frappe.db.exists("User", email):
		user = frappe.get_doc(
			{
				"doctype": "User",
				"email": email,
				"first_name": email.split("@")[0],
				"enabled": 1,
				"user_type": "Website User",
				"send_welcome_email": 0,
			}
		)
		user.flags.ignore_permissions = True
		user.insert()
		user.add_roles("Customer")

	if customer and not frappe.db.exists(
		"Portal User", {"parenttype": "Customer", "parent": customer, "user": email}
	):
		doc = frappe.get_doc("Customer", customer)
		doc.append("portal_users", {"user": email})
		doc.save(ignore_permissions=True)

	return email


def _visit_request(customer):
	doc = frappe.get_doc(
		{
			"doctype": "Visit Request",
			"customer": customer,
			"company": COMPANY,
			"request_by_date": frappe.utils.nowdate(),
			"request_by_time": "10:00:00",
			"status": "Open",
		}
	)
	# operation_order is mandatory and Operation Order is readable only by
	# System Manager; none exist on this site. Access control is what is under
	# test here, not document completeness.
	doc.flags.ignore_mandatory = True
	doc.insert(ignore_permissions=True)
	return doc.name


class TestVisitRequestPermissions(FrappeTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		_customer(CUSTOMER_A)
		_customer(CUSTOMER_B)
		_portal_user(USER_A, CUSTOMER_A)
		_portal_user(USER_B, CUSTOMER_B)
		_portal_user(USER_UNLINKED)
		cls.request_a = _visit_request(CUSTOMER_A)
		cls.request_b = _visit_request(CUSTOMER_B)
		# Deliberately no commit: IntegrationTestCase registers a class-level
		# rollback, so these fixtures disappear when the class finishes. This
		# suite runs against the developer's real site.

	def tearDown(self):
		frappe.set_user("Administrator")

	# --- lists -------------------------------------------------------------
	# All of these use frappe.get_list, not get_all: get_all passes
	# ignore_permissions=True and would happily return every row, proving
	# nothing. get_list is what /api/resource and the portal actually call.

	def test_customer_lists_only_their_own(self):
		frappe.set_user(USER_A)
		names = frappe.get_list("Visit Request", pluck="name")
		self.assertIn(self.request_a, names)
		self.assertNotIn(self.request_b, names)

	def test_unlinked_portal_user_sees_nothing(self):
		"""Registered but not yet attached to a Customer: zero rows, not all."""
		frappe.set_user(USER_UNLINKED)
		self.assertEqual(frappe.get_list("Visit Request", pluck="name"), [])

	def test_query_condition_denies_rather_than_returning_empty_string(self):
		"""An empty condition means 'no filter', which would expose everything."""
		frappe.set_user(USER_UNLINKED)
		self.assertEqual(visit_request_query(USER_UNLINKED), "1=0")

	def test_staff_are_not_filtered(self):
		self.assertEqual(visit_request_query("Administrator"), "")
		frappe.set_user("Administrator")
		names = frappe.get_list("Visit Request", pluck="name")
		self.assertIn(self.request_a, names)
		self.assertIn(self.request_b, names)

	# --- single document ---------------------------------------------------

	def test_customer_cannot_open_another_customers_request(self):
		"""The path query conditions never see: fetching by name."""
		frappe.set_user(USER_A)
		with self.assertRaises(frappe.PermissionError):
			frappe.get_doc("Visit Request", self.request_b).check_permission("read")

	def test_customer_can_open_their_own_request(self):
		frappe.set_user(USER_A)
		doc = frappe.get_doc("Visit Request", self.request_a)
		self.assertTrue(visit_request_has_permission(doc, "read", USER_A))

	def test_has_permission_denies_across_customers(self):
		doc = frappe.get_doc("Visit Request", self.request_b)
		frappe.set_user(USER_A)
		self.assertFalse(visit_request_has_permission(doc, "read", USER_A))

	# --- write paths -------------------------------------------------------

	def test_customer_cannot_delete_or_write(self):
		"""Cancelling is a status change made by staff; the record is history."""
		frappe.set_user(USER_A)
		self.assertFalse(frappe.has_permission("Visit Request", "delete"))
		self.assertFalse(frappe.has_permission("Visit Request", "write"))
		self.assertFalse(frappe.has_permission("Visit Request", "create"))

	# --- portal detail view ------------------------------------------------

	def test_website_permission_scopes_the_portal_detail_view(self):
		"""frappe.has_website_permission() returns False with no hook at all,
		so this also proves the hook is registered."""
		frappe.set_user(USER_A)
		self.assertTrue(frappe.has_website_permission(frappe.get_doc("Visit Request", self.request_a)))
		frappe.set_user("Administrator")
		doc_b = frappe.get_doc("Visit Request", self.request_b)
		frappe.set_user(USER_A)
		self.assertFalse(frappe.has_website_permission(doc_b))
