from frappe.www.me import get_context as _get_context

# Frappe resolves a www page's Python controller from the SAME app where the
# matching .html was found (TemplatePage.set_pymodule), not from wherever
# the original template lived — so overriding only me.html (without this
# file) silently skips frappe.www.me.get_context() entirely, leaving
# `current_user` undefined. Delegating here keeps the original context logic
# (Guest guard, is_portal_user, etc.) completely untouched.
no_cache = 1


def get_context(context):
	return _get_context(context)
