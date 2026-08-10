import frappe
from frappe.utils import cint
from frappe.www.login import sanitize_redirect

from pestcontrol.pc_website.utils import get_website_context


def get_context(context):
	get_website_context(context)
	context.no_cache = 1

	if frappe.session.user != "Guest":
		frappe.local.flags.redirect_location = "/"
		raise frappe.Redirect

	context.redirect_to = sanitize_redirect(frappe.local.form_dict.get("redirect-to")) or ""
	context.disable_signup = cint(frappe.get_website_settings("disable_signup"))
