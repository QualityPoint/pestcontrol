import frappe

from pestcontrol.pc_website.utils import get_website_context


def _default_currency():
	company = frappe.defaults.get_global_default("company")
	if company:
		return frappe.get_cached_value("Company", company, "default_currency") or "SAR"
	return "SAR"


def get_context(context):
	get_website_context(context)
	context.no_cache = 1
	# Positions offered on the careers form come straight from HRMS Job
	# Openings — admins create them there, tick "Publish on website" (publish)
	# and set Status = Open to make them selectable here. Same filter HRMS's
	# own /jobs portal uses.
	context.job_openings = frappe.get_all(
		"Job Opening",
		filters={"status": "Open", "publish": 1},
		fields=["name", "job_title", "location", "department"],
		order_by="posted_on desc",
	)
	# Reference data for the redesigned form's selects. Applications become
	# HRMS Job Applicant records, so these mirror that doctype's country /
	# currency link targets.
	context.countries = frappe.get_all("Country", pluck="name", order_by="name asc")
	context.currencies = frappe.get_all("Currency", filters={"enabled": 1}, pluck="name", order_by="name asc")
	context.default_country = frappe.db.get_default("country") or "Saudi Arabia"
	context.default_currency = _default_currency()
