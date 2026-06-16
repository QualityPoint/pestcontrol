# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import time_diff_in_seconds


@frappe.whitelist()
def calculate_duration(from_time=None, to_time=None):
	"""Return the duration in seconds between two datetimes (for a Duration field).

	Both ends are full datetimes, so a visit that crosses midnight
	(e.g. 23:00 -> 00:30 the next day) is measured correctly with a plain diff.

	Returns 0 when either value is missing or when ``to_time`` is not strictly
	after ``from_time`` (treated as not-yet-entered / invalid rather than an error).
	"""
	if not from_time or not to_time:
		return 0

	seconds = time_diff_in_seconds(to_time, from_time)
	return seconds if seconds > 0 else 0
