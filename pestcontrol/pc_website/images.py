# Copyright (c) 2026, QualityPoint and contributors
# For license information, please see license.txt

"""Keep uploaded images from arriving at camera resolution.

The theme's own photos were re-encoded once, but that fixes 16 static files
and nothing else. Every image an admin attaches through the desk -- service
images, blog covers, hero backgrounds, branch photos -- lands in /files/ via
the File doctype, and frappe never optimises those: `optimize_image()` exists
and `File.optimize_file()` wraps it, but nothing in the framework calls it.
Without this hook the site's weight creeps back up as content is added.

Reuses frappe.utils.image.optimize_image rather than hand-rolling. It already
returns the original when optimising made the file bigger, which is the guard
that actually matters.
"""

import mimetypes

import frappe
from frappe.utils.image import optimize_image

# Same ceiling as the re-encoded theme assets, so both pipelines agree. The
# site's container maxes at 1300px, so 1600 still covers a full-width hero on
# a retina screen.
MAX_EDGE = 1600

# Only content that ends up on the public website. An invoice attachment or a
# scanned document has no business being silently resized.
WEBSITE_DOCTYPES = {
	"PC Website Settings", "Website Service", "Website Project", "Website Blog Post",
	"Website Pest", "Website Team Member", "Website Branch", "Website Hero Slide",
	"Website Gallery Item", "Website Testimonial", "Website City", "Website Article",
}


def optimize_website_upload(doc, method=None):
	"""`File.after_insert` hook."""
	if not _should_optimize(doc):
		return

	content_type = mimetypes.guess_type(doc.file_name)[0] or ""
	original = _content_bytes(doc)
	if original is None:
		return

	optimized = optimize_image(
		content=original,
		content_type=content_type,
		max_width=MAX_EDGE,
		max_height=MAX_EDGE,
	)
	if optimized is original or len(optimized) >= len(original):
		return

	doc.save_file(content=optimized, overwrite=True)
	doc.save(ignore_permissions=True)


def _should_optimize(doc):
	if doc.is_folder or not doc.file_name or not doc.file_size:
		return False
	if doc.attached_to_doctype not in WEBSITE_DOCTYPES:
		return False

	content_type = mimetypes.guess_type(doc.file_name)[0] or ""
	if not content_type.startswith("image/"):
		return False
	# SVG is vector: resizing is meaningless and optimize_image no-ops on it.
	if content_type == "image/svg+xml":
		return False

	# Already small enough. Checked so that re-saving a record does not send
	# the same photo through a lossy encoder again and again, degrading it a
	# little each time.
	return _exceeds_ceiling(doc)


def _exceeds_ceiling(doc):
	content = _content_bytes(doc)
	if content is None:
		return False
	try:
		from io import BytesIO

		from PIL import Image

		with Image.open(BytesIO(content)) as image:
			return max(image.size) > MAX_EDGE
	except Exception:
		# If the dimensions cannot be read, leave the file alone rather than
		# guess -- a corrupt or exotic format should pass through untouched.
		return False


def _content_bytes(doc):
	"""Raw file bytes, with frappe's text decoding switched off.

	File.get_content() is typed `bytes | str`: it walks FILE_ENCODING_OPTIONS
	and returns a str the moment one of them succeeds. Binary image data can
	decode "successfully" that way, and the result does NOT round-trip -- a
	800x600 PNG here came back as a 2791-character str whose re-encoding no
	longer matches the file. Optimising that and saving it would have written
	a corrupt image over the user's upload.

	Passing `encodings=[]` skips the decode loop entirely and hands back the
	bytes on disk, verified byte-identical to the original.
	"""
	try:
		content = doc.get_content(encodings=[])
	except Exception:
		# Unreadable or already gone; never block an upload over it.
		return None
	return content if isinstance(content, bytes) else None
