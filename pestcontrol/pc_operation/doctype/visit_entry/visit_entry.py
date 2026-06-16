# Copyright (c) 2026, QP and contributors
# For license information, please see license.txt

from datetime import datetime

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import format_datetime, get_datetime, time_diff_in_seconds

from pestcontrol.utils import calculate_duration


class VisitEntry(Document):
    def validate(self):
        self.validate_operation_order()
        self.validate_supervisor()
        self.validate_worker_company()
        self.sort_timesheet()
        self.validate_timesheet_overlap()
        self.validate_worker_overlap()
        self.validate_worker_times_within_visit()
        self.validate_amenity_pest_types()
        self.validate_chemicals()

    def before_submit(self):
        self.validate_required_tables(("amenities", "chemicals"))
        self.validate_and_set_durations()
        self.set_visit_totals()

    def on_submit(self):
        self.db_set("status", "Completed")

    def on_cancel(self):
        self.db_set("status", "Cancelled")

    # ------------------------------------------------------------------ #
    # validations                                                        #
    # ------------------------------------------------------------------ #

    def sort_timesheet(self):
        """Keep the timesheet ordered chronologically by `from_time` (ascending).

        Rows without a `from_time` yet (still being entered) sink to the bottom
        so they don't break the chronological run; `idx` is renumbered to persist
        the order.
        """
        rows = self.timesheet or []
        rows.sort(key=lambda row: get_datetime(row.from_time) if row.from_time else datetime.max)
        for idx, row in enumerate(rows, start=1):
            row.idx = idx

    def validate_operation_order(self):
        """The linked Operation Order must be submitted and belong to this visit's
        customer and company.

        The client `set_query` enforces the same filter, but the server never
        trusts the client (API writes, imports, programmatic changes).
        """
        if not self.operation_order:
            return

        order = frappe.db.get_value(
            "Operation Order", self.operation_order, ("customer", "company", "docstatus"), as_dict=True
        )

        if order.docstatus != 1:
            frappe.throw(_("Operation Order {0} must be submitted.").format(frappe.bold(self.operation_order)))

        for fieldname in ("customer", "company"):
            if order.get(fieldname) != self.get(fieldname):
                frappe.throw(
                    _("Operation Order {0} does not belong to the selected {1} ({2}).").format(
                        frappe.bold(self.operation_order),
                        _(self.meta.get_label(fieldname)),
                        frappe.bold(self.get(fieldname) or ""),
                    )
                )

    def validate_supervisor(self):
        """The supervisor must belong to this visit's company and be flagged as a
        supervisor (mirrors the client `set_query`)."""
        if not self.supervisor:
            return

        worker = frappe.db.get_value(
            "Operation Worker", self.supervisor, ("company", "is_supervisor"), as_dict=True
        )
        if not worker.is_supervisor:
            frappe.throw(_("{0} is not a supervisor.").format(frappe.bold(self.supervisor)))
        if worker.company != self.company:
            frappe.throw(
                _("Supervisor {0} does not belong to company {1}.").format(
                    frappe.bold(self.supervisor), frappe.bold(self.company or "")
                )
            )

    def validate_worker_company(self):
        """Every worker must belong to this visit's company (mirrors the client
        `set_query`). Resolved in a single query for all rows."""
        names = {row.worker for row in self.workers if row.worker}
        if not names:
            return

        company_of = dict(
            frappe.get_all(
                "Operation Worker", filters={"name": ("in", names)}, fields=["name", "company"], as_list=True
            )
        )
        for row in self.workers:
            if row.worker and company_of.get(row.worker) != self.company:
                self._row_throw(
                    row,
                    _("Worker {0} does not belong to company {1}.").format(
                        frappe.bold(row.worker_name or row.worker), frappe.bold(self.company or "")
                    ),
                )

    def validate_timesheet_overlap(self):
        """Timesheet intervals must not overlap (touching boundaries allowed)."""
        self._check_interval_overlap(self.timesheet)

    def validate_worker_overlap(self):
        """Each worker's own intervals must not overlap.

        A worker may appear in several rows — e.g. clocked out for a break and
        back again — but those stints cannot clash. Rows are grouped by `worker`
        and each group is checked independently.
        """
        groups = {}
        for row in self.workers:
            if row.worker:
                groups.setdefault(row.worker, []).append(row)

        for rows in groups.values():
            context = _("Worker {0} — ").format(rows[0].worker_name or rows[0].worker)
            self._check_interval_overlap(rows, context)

    def validate_worker_times_within_visit(self):
        """Workers must operate within the visit's time window.

        The window is [earliest timesheet `from_time`, latest timesheet
        `to_time`]. A worker cannot start before the visit starts, nor finish
        after it ends. Rows lacking the relevant bound (still in progress /
        draft) are skipped; full presence is enforced at submit.
        """
        visit_start, visit_end = self._timesheet_window()

        for row in self.workers:
            if visit_start and row.from_time and get_datetime(row.from_time) < visit_start:
                self._row_throw(
                    row,
                    _("From Time ({0}) cannot be before the visit start ({1}).").format(
                        format_datetime(row.from_time), format_datetime(visit_start)
                    ),
                )
            if visit_end and row.to_time and get_datetime(row.to_time) > visit_end:
                self._row_throw(
                    row,
                    _("To Time ({0}) cannot be after the visit end ({1}).").format(
                        format_datetime(row.to_time), format_datetime(visit_end)
                    ),
                )

    def validate_amenity_pest_types(self):
        """Guarantee every amenity row has at least one pest type.

        `pest_type` is read-only (edited via the pills control), so enforce the
        mandatory rule on the server rather than relying on the client.
        """
        for row in self.amenities:
            if not (row.pest_type or "").strip():
                self._row_throw(
                    row, _("select at least one Pest Type for amenity {0}.").format(frappe.bold(row.amenity or ""))
                )

    def validate_required_tables(self, fieldnames):
        """Require at least one row in each of the given child tables (at submit)."""
        for fieldname in fieldnames:
            if not self.get(fieldname):
                frappe.throw(
                    _("Add at least one row in {0}.").format(frappe.bold(_(self.meta.get_label(fieldname))))
                )

    def validate_chemicals(self):
        """Validate and resolve each chemical line, the same way ERPNext does.

        Per row (a single pass over the table): `qty` must be positive;
        `chemical_name`/`stock_uom` arrive via `fetch_from`; the transaction
        `uom` defaults to the stock UOM and the read-only `conversion_factor` is
        set from the item (never trusting the client), rejecting any UOM with no
        conversion defined for the item.
        """
        from erpnext.stock.get_item_details import get_conversion_factor

        for row in self.chemicals:
            if not row.chemical_item:
                continue

            if (row.qty or 0) <= 0:
                self._row_throw(row, _("Quantity must be greater than zero."))

            if not row.uom:
                sales_uom, stock_uom = frappe.db.get_value(
                    "Item", row.chemical_item, ("sales_uom", "stock_uom")
                )
                row.uom = sales_uom or stock_uom

            factor = get_conversion_factor(row.chemical_item, row.uom).get("conversion_factor")
            if not factor:
                self._row_throw(
                    row,
                    _("UOM {0} is not valid for item {1}. Add it to the item's UOM Conversion table.").format(
                        frappe.bold(row.uom), frappe.bold(row.chemical_item)
                    ),
                )
            row.conversion_factor = factor

    def validate_and_set_durations(self):
        """Validate time ranges and (re)compute durations — at submit only.

        `to_time` may be unknown while a visit is in progress, so these checks
        run on submit. Per row we require the configured time fields, ensure
        `to_time` is strictly after `from_time` (full datetimes, so a
        midnight-crossing range is valid), and recompute `duration` server-side
        — the client's live value is never trusted.
        """
        self._validate_time_rows(self.timesheet, required=("to_time",))
        self._validate_time_rows(self.workers, required=("from_time", "to_time"))

    # ------------------------------------------------------------------ #
    # roll-ups                                                           #
    # ------------------------------------------------------------------ #

    def set_visit_totals(self):
        """Roll up the timesheet intervals into the visit summary fields.

        Runs at submit, after `validate_and_set_durations` has refreshed each
        row's `duration`:
          - interval_count: number of timesheet rows.
          - visit_duration: total worked time = sum of the intervals' durations.
          - visit_timeout: idle time = visit window span − visit_duration
            (clamped at 0 if intervals overlap).
        """
        rows = self.timesheet or []
        self.interval_count = len(rows)
        self.visit_duration = sum(row.duration or 0 for row in rows)

        visit_start, visit_end = self._timesheet_window()
        if visit_start and visit_end:
            span = time_diff_in_seconds(visit_end, visit_start)
            self.visit_timeout = max(span - self.visit_duration, 0)
        else:
            self.visit_timeout = 0

    # ------------------------------------------------------------------ #
    # helpers                                                            #
    # ------------------------------------------------------------------ #

    def _timesheet_window(self):
        """Return (visit_start, visit_end) datetimes from the timesheet.

        Either bound is ``None`` when no row carries the corresponding time yet.
        """
        starts = [get_datetime(row.from_time) for row in self.timesheet if row.from_time]
        ends = [get_datetime(row.to_time) for row in self.timesheet if row.to_time]
        return (min(starts) if starts else None, max(ends) if ends else None)

    def _validate_time_rows(self, rows, required):
        """Require the given time fields and reject inverted ranges, per row."""
        for row in rows or []:
            for fieldname in required:
                if not row.get(fieldname):
                    self._row_throw(row, _("{0} is required.").format(_(row.meta.get_label(fieldname))))

            if row.from_time and row.to_time and time_diff_in_seconds(row.to_time, row.from_time) <= 0:
                self._row_throw(
                    row,
                    _("To Time ({0}) must be after From Time ({1}).").format(
                        format_datetime(row.to_time), format_datetime(row.from_time)
                    ),
                )

            row.duration = calculate_duration(row.from_time, row.to_time)

    def _check_interval_overlap(self, rows, context=""):
        """Reject overlapping [from_time, to_time] intervals among ``rows``.

        Sorts the complete rows by `from_time`, then a single pass flags any
        interval that starts before the previous one ends. Touching boundaries
        are allowed (strict overlap only); rows missing a time are skipped.
        ``context`` optionally prefixes the message (e.g. a worker's name).
        """
        intervals = sorted(
            (row for row in rows if row.from_time and row.to_time),
            key=lambda row: get_datetime(row.from_time),
        )
        previous = None
        for row in intervals:
            if previous and get_datetime(row.from_time) < get_datetime(previous.to_time):
                self._row_throw(
                    row,
                    _("{0}Interval ({1} - {2}) overlaps the previous one ({3} - {4}).").format(
                        context,
                        format_datetime(row.from_time),
                        format_datetime(row.to_time),
                        format_datetime(previous.from_time),
                        format_datetime(previous.to_time),
                    ),
                )
            previous = row

    @staticmethod
    def _row_throw(row, message):
        """Raise a row-prefixed error: '<Child DocType> Row #<idx>: <message>'."""
        frappe.throw(_("{0} Row #{1}: {2}").format(_(row.doctype), row.idx, message))
