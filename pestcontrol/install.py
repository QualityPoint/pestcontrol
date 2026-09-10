import click
import frappe

from pestcontrol.setup import after_install as setup


def after_install():
	try:
		print("Setting up PestControl...")
		setup()

		click.secho("Thank you for installing PestControl!", fg="green")

	except Exception as e:
		BUG_REPORT_URL = "https://github.com/QualityPoint/pestcontrol/issues/new"
		click.secho(
			"Installation for PestControl app failed due to an error."
			" Please try re-installing the app or"
			f" report the issue on {BUG_REPORT_URL} if not resolved.",
			fg="bright_red",
		)
		raise e


def before_tests():
	# Both settings are normally configured by hand (disable_signup via the
	# desk, default_role via ERPNext's interactive setup wizard) -- neither
	# ever runs on a freshly installed site, which is what CI tests against.
	# `bench run-tests --app pestcontrol` only loads pestcontrol's own hooks,
	# so this is the only before_tests that will ever fire here; frappe's own
	# (which would otherwise do the disable_signup half of this) also no-ops
	# whenever more than one app is installed, which CI always does.
	frappe.db.set_single_value("Website Settings", "disable_signup", 0)
	if not frappe.get_single_value("Portal Settings", "default_role"):
		frappe.db.set_single_value("Portal Settings", "default_role", "Customer")
	# Required, not defensive: before_tests runs once, outside any individual
	# test's own transaction, and mirrors frappe's own before_tests (which
	# does the same commit) for exactly that reason -- later test classes,
	# each with their own rollback-to-savepoint, must see this as committed
	# baseline state rather than something a later rollback could undo.
	frappe.db.commit()  # nosemgrep: frappe-manual-commit
	frappe.clear_cache()
