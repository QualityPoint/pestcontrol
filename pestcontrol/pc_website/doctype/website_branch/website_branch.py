# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

import re

from frappe.model.document import Document

from pestcontrol.pc_website.utils import validate_articles

# Google's embed URLs carry the map centre inside the `pb` parameter, where
# !2d is the longitude and !3d the latitude:
#
#   ...!1m3!1d371.7!2d39.64607786133927!3d24.48846581276346!2m3!1f0...
#
# Undocumented, so both patterns are matched independently and a miss simply
# leaves the field alone.
_EMBED_LONGITUDE = re.compile(r"!2d(-?\d+\.\d+)")
_EMBED_LATITUDE = re.compile(r"!3d(-?\d+\.\d+)")


class WebsiteBranch(Document):
	def validate(self):
		validate_articles(self)
		self.set_coordinates_from_map_url()

	def set_coordinates_from_map_url(self):
		"""Fill latitude/longitude from the pasted Google Maps embed URL.

		The embed URL and the coordinates look redundant but serve different
		readers: the URL renders the visible map, while the coordinates are
		what goes into LocalBusiness structured data as a factual claim about
		where the business is -- google does not read a position out of a
		third-party iframe. Since the URL already contains the centre point,
		deriving it here means the admin pastes one thing rather than two.

		Only fills blanks, so a hand-corrected pin is never overwritten.
		Silently does nothing when the URL is missing or in a format we do not
		recognise: a wrong coordinate would publish the branch at the wrong
		address, which is worse than publishing none.
		"""
		if self.latitude and self.longitude:
			return
		if not self.map_embed_url:
			return

		latitude = _EMBED_LATITUDE.search(self.map_embed_url)
		longitude = _EMBED_LONGITUDE.search(self.map_embed_url)
		if not (latitude and longitude):
			return

		# Guard against a pattern that matched something that is not a
		# coordinate -- the `pb` blob holds plenty of other !<n>d numbers.
		lat, lng = float(latitude.group(1)), float(longitude.group(1))
		if not (-90 <= lat <= 90 and -180 <= lng <= 180):
			return

		self.latitude = lat
		self.longitude = lng
