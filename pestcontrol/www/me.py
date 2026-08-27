from frappe.sessions import get_csrf_token
from frappe.www.me import get_context as _get_context

# Frappe resolves a www page's Python controller from the SAME app where the
# matching .html was found (TemplatePage.set_pymodule), not from wherever
# the original template lived — so overriding only me.html (without this
# file) silently skips frappe.www.me.get_context() entirely, leaving
# `current_user` undefined. Delegating here keeps the original context logic
# (Guest guard, is_portal_user, etc.) completely untouched.
no_cache = 1


def get_context(context):
	_get_context(context)
	# Must happen here, not via a jinja method: generating a token for a
	# session that doesn't have one yet is a DB write (session_obj.update),
	# and Jinja template rendering runs under a read-only SQL guard —
	# calling get_csrf_token() directly from the template throws
	# "Read-Only queries are allowed" the first time a session needs one.
	context.csrf_token = get_csrf_token()
	return context
