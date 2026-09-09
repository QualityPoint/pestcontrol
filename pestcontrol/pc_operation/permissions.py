# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

"""Row-level access to Visit Request for portal customers.

The `Customer` role is granted to every self-registered website user -- it is
`Portal Settings.default_role` -- and it holds a direct DocPerm on Visit
Request. A DocPerm on its own is doctype-wide: `if_owner` is 0, there are no
User Permissions on this site, and nothing else narrowed it, so any registered
visitor could read every customer's visit requests through
`/api/resource/Visit Request`.

ERPNext does not have this problem for quotations and invoices because it
grants portal users no DocPerm at all and serves those through
`get_transaction_list`, scoping by Portal User. Visit Request is a pestcontrol
doctype that took the DocPerm route instead, so the equivalent scoping is
supplied here -- reusing erpnext's Portal User lookup rather than inventing a
second notion of "this user's customers".

Both hooks are needed, because they cover different code paths:

  * `permission_query_conditions` filters *lists* -- the portal, the API list
    endpoint, search.
  * `has_permission` covers a *single document* fetched by name, which query
    conditions never see.

A third gate lives in hooks.py: `has_website_permission`, pointed straight at
erpnext's own generic implementation. Frappe returns False when no such hook is
registered, so without it the portal's detail view would refuse a customer
their own record.
"""

import frappe
from frappe.utils.user import is_website_user


def visit_request_query(user=None):
	"""`permission_query_conditions` hook for Visit Request."""
	user = user or frappe.session.user
	if not is_website_user(user):
		# Staff keep whatever their own DocPerms already grant.
		return ""

	customers = _customers_for_user()
	if not customers:
		# Registered but not linked to any customer yet: show nothing rather
		# than everything. A portal user with no Customer has no business
		# seeing another company's visits.
		return "1=0"

	joined = ", ".join(frappe.db.escape(c) for c in customers)
	return f"`tabVisit Request`.`customer` in ({joined})"


def visit_request_has_permission(doc, ptype="read", user=None):
	"""`has_permission` hook for Visit Request.

	Guards the single-document path -- opening a record by name through the
	REST API or the desk -- which `permission_query_conditions` never reaches.
	Controller hooks can only deny, never grant, so this cannot widen access
	for anyone.
	"""
	user = user or frappe.session.user
	if not is_website_user(user):
		return True

	customers = _customers_for_user()
	return bool(customers) and doc.get("customer") in customers


def _customers_for_user():
	"""Customers the current portal user is linked to, via Portal User.

	The same source erpnext's own portal uses, so a customer sees a consistent
	set of records across visit requests, quotations and invoices instead of
	two definitions drifting apart.
	"""
	from erpnext.controllers.website_list_for_contact import get_parents_for_user

	return get_parents_for_user("Customer") or []
