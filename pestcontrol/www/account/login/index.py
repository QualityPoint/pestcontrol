import frappe
from frappe.utils import cint
from frappe.website.utils import get_home_page
from frappe.www.login import sanitize_redirect

from pestcontrol.pc_website.utils import get_website_context


def get_context(context):
	get_website_context(context)
	context.no_cache = 1

	redirect_to = sanitize_redirect(frappe.local.form_dict.get("redirect-to"))

	if frappe.session.user != "Guest":
		if not redirect_to:
			redirect_to = "/app" if frappe.session.data.user_type != "Website User" else (get_home_page() or "/")
		frappe.local.flags.redirect_location = redirect_to
		raise frappe.Redirect

	context.redirect_to = redirect_to or ""
	context.disable_signup = cint(frappe.get_website_settings("disable_signup"))
