from erpnext.templates.pages.order import get_context as _get_context

# Same reason as pestcontrol/www/me.py: overriding only order.html leaves
# erpnext's get_context() (permission check, payment/loyalty details, etc.)
# unresolved and never called. Delegate to it unchanged.
no_cache = 1


def get_context(context):
	return _get_context(context)
