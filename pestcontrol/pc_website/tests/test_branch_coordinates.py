# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

"""Tests for deriving branch coordinates from a Google Maps embed URL.

The failure mode that matters is not "did not parse" -- that just leaves the
fields blank for an admin to fill. It is parsing something *wrong*, which
would publish the branch at an address it is not at, as structured fact.
"""

import frappe
from frappe.tests.utils import FrappeTestCase


def _branch(**kwargs):
	doc = frappe.new_doc("Website Branch")
	doc.update(kwargs)
	return doc


# The real URL from the Medina branch: !2d longitude, !3d latitude.
MEDINA = (
	"https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d371.70110356253355"
	"!2d39.64607786133927!3d24.48846581276346!2m3!1f0!2f0!3f0!3m2!1i1024!2i768"
	"!4f13.1!5e1!3m2!1sen!2ssa!4v1786882793365!5m2!1sen!2ssa"
)


class TestBranchCoordinates(FrappeTestCase):
	def test_extracts_coordinates_from_embed_url(self):
		branch = _branch(map_embed_url=MEDINA)
		branch.set_coordinates_from_map_url()
		self.assertAlmostEqual(branch.latitude, 24.48846581276346, places=6)
		self.assertAlmostEqual(branch.longitude, 39.64607786133927, places=6)

	def test_does_not_overwrite_a_hand_placed_pin(self):
		branch = _branch(map_embed_url=MEDINA, latitude=24.5, longitude=39.5)
		branch.set_coordinates_from_map_url()
		self.assertEqual(branch.latitude, 24.5)
		self.assertEqual(branch.longitude, 39.5)

	def test_fills_in_when_only_one_coordinate_is_present(self):
		"""Half-filled is as unusable as empty, so it is completed."""
		branch = _branch(map_embed_url=MEDINA, latitude=0, longitude=0)
		branch.set_coordinates_from_map_url()
		self.assertAlmostEqual(branch.latitude, 24.48846581276346, places=6)

	def test_unrecognised_url_leaves_fields_untouched(self):
		"""A guess would put the business at the wrong address."""
		for url in ("https://maps.app.goo.gl/abc123",
		            "https://www.google.com/maps/place/Riyadh",
		            "not a url at all", ""):
			with self.subTest(url=url):
				branch = _branch(map_embed_url=url)
				branch.set_coordinates_from_map_url()
				self.assertFalse(branch.latitude)
				self.assertFalse(branch.longitude)

	def test_no_url_at_all_is_harmless(self):
		branch = _branch()
		branch.set_coordinates_from_map_url()
		self.assertFalse(branch.latitude)

	def test_out_of_range_values_are_rejected(self):
		"""The pb blob is full of other !<n>d numbers; only plausible ones win."""
		branch = _branch(map_embed_url="!2d999.123456!3d888.123456")
		branch.set_coordinates_from_map_url()
		self.assertFalse(branch.latitude)
		self.assertFalse(branch.longitude)

	def test_negative_coordinates_survive(self):
		"""Western/southern hemispheres are valid, if unlikely for this client."""
		branch = _branch(map_embed_url="!1d100.0!2d-58.381592!3d-34.603722!2m3")
		branch.set_coordinates_from_map_url()
		self.assertAlmostEqual(branch.latitude, -34.603722, places=6)
		self.assertAlmostEqual(branch.longitude, -58.381592, places=6)

	# validate() must run it, or none of the above reaches the database.
	def test_validate_triggers_derivation(self):
		branch = _branch(map_embed_url=MEDINA, phone="+966 5 000 0000")
		branch.append("article", {"language": "en", "title": "Test Branch"})
		branch.validate()
		self.assertAlmostEqual(branch.latitude, 24.48846581276346, places=6)
