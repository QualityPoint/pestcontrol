import frappe

from pestcontrol.pc_website.utils import get_website_context


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
