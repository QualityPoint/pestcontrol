from frappe.sessions import get_csrf_token
from frappe.www.portal import get_context as _get_context

# Same reason as pestcontrol/www/me.py: overriding only portal.html without
# this file means frappe.www.portal.get_context() never runs for a plain
# TemplatePage render (only /orders, /quotations, /invoices are spared,
# since those route through list_renderer.py's ListPage, a different code
# path that resolves the context explicitly). Bare /portal never crashed on
# this gap only because nothing in that path needs a doctype/raw_result
# context var — but it also means get_csrf_token() genuinely needs
# generating here, not assumed already present.
no_cache = 1


def get_context(context, **dict_params):
	_get_context(context, **dict_params)
	context.csrf_token = get_csrf_token()
	return context
