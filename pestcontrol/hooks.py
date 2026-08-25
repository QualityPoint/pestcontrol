app_name = "pestcontrol"
app_title = "Pest Control"
app_publisher = "QualityPoint"
app_description = "A comprehensive pest control management system built on Frappe, streamlining service scheduling, technician dispatch, chemical inventory tracking, and client reporting"
app_email = "erp@qp.sa"
app_license = "gpl-3.0"

# Apps
# ------------------

required_apps = ["erpnext"]

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "pestcontrol",
# 		"logo": "/assets/pestcontrol/logo.png",
# 		"title": "Pest Control",
# 		"route": "/pestcontrol",
# 		"has_permission": "pestcontrol.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/pestcontrol/css/pestcontrol.css"
app_include_js = "pestcontrol.bundle.js"

# include js, css files in header of web template
web_include_css = "/assets/pestcontrol/website/css/portal.css"
# web_include_js = "/assets/pestcontrol/js/pestcontrol.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "pestcontrol/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "pestcontrol/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "home"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
website_generators = ["Website Service", "Website Project", "Website Team Member", "Website Blog Post"]


# Fixtures
# ----------

# Deliberately does NOT include the website CMS content doctypes (PC
# Website Settings, Website Service, Website Blog Post, etc). They used to
# be listed here so a fresh install wasn't empty, but once the site went
# live, that became actively harmful: `bench migrate` re-imports every
# fixture unconditionally on every run, so any live edit made directly on
# production (a new photo, a service description tweak, an About page
# change...) would get silently overwritten back to whatever the last
# `bench export-fixtures` snapshot in this repo happened to contain the
# next time code was deployed. Production's database is now the sole
# source of truth for all of that content — nothing here pushes into it.
# Only genuinely static, identical-everywhere reference data belongs in
# this list.
# fixtures = [
# 	{"dt": "Language", "filters": [["name", "in", ["en", "ar"]]]},
# ]

# Jinja
# ----------

# add methods and filters to jinja environment
jinja = {
	"methods": [
		"pestcontrol.pc_website.utils.localize",
		"pestcontrol.pc_website.utils.asset_version",
		"pestcontrol.pc_website.utils.doc_to_json",
		"pestcontrol.pc_website.utils.portal_user_info",
	],
}

# Installation
# ------------

# before_install = "pestcontrol.install.before_install"
after_install = "pestcontrol.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "pestcontrol.uninstall.before_uninstall"
# after_uninstall = "pestcontrol.uninstall.after_uninstall"

# Site Migration
# --------------

# before_migrate = "pestcontrol.install.before_install"
# after_migrate = "pestcontrol.install.after_install"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "pestcontrol.utils.before_app_install"
# after_app_install = "pestcontrol.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "pestcontrol.utils.before_app_uninstall"
# after_app_uninstall = "pestcontrol.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "pestcontrol.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Session
# ---------------

# ERPNext's own on_session_creation (create_customer_or_supplier) links a
# self-registered customer's Contact to a Customer but never adds them to
# that Customer's Portal User table — which is what the customer portal
# (and the pestcontrol dashboard) actually filters on. Without this, a
# self-registered customer's own Orders/Quotations/Invoices stay invisible
# to them. See pestcontrol.pc_website.utils.sync_portal_user_on_login.
on_session_creation = "pestcontrol.pc_website.utils.sync_portal_user_on_login"

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"pestcontrol.tasks.all"
# 	],
# 	"daily": [
# 		"pestcontrol.tasks.daily"
# 	],
# 	"hourly": [
# 		"pestcontrol.tasks.hourly"
# 	],
# 	"weekly": [
# 		"pestcontrol.tasks.weekly"
# 	],
# 	"monthly": [
# 		"pestcontrol.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "pestcontrol.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "pestcontrol.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "pestcontrol.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["pestcontrol.utils.before_request"]
# after_request = ["pestcontrol.utils.after_request"]

# Job Events
# ----------
# before_job = ["pestcontrol.utils.before_job"]
# after_job = ["pestcontrol.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"pestcontrol.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
