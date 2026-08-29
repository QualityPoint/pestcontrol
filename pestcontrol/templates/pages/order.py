from erpnext.templates.pages.order import get_context as _get_context
from frappe.sessions import get_csrf_token

# Same reason as pestcontrol/www/me.py: overriding only order.html leaves
# erpnext's get_context() (permission check, payment/loyalty details, etc.)
# unresolved and never called. Delegate to it unchanged.
no_cache = 1


def get_context(context):
	_get_context(context)
	# See pestcontrol/www/me.py — must generate the token here (Python), not
	# via a jinja method, since a fresh session needs a DB write to get one.
	context.csrf_token = get_csrf_token()
	return context
