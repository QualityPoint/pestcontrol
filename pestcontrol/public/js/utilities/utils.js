frappe.provide("pestcontrol.utils");

pestcontrol.utils = {
	/**
	 * Calculate the duration (in seconds, for a Duration field) between two
	 * datetime values by delegating to the server method of the same name.
	 *
	 * Both ends are full datetimes, so a visit that crosses midnight
	 * (e.g. "2026-06-16 23:00:00" -> "2026-06-17 00:30:00") is handled correctly.
	 * Resolves to 0 when either value is missing or the range is inverted.
	 *
	 * @param {string} from_time  Datetime string, e.g. "2026-06-16 23:00:00"
	 * @param {string} to_time    Datetime string
	 * @returns {Promise<number>} duration in seconds
	 */
	calculate_duration(from_time, to_time) {
		// short-circuit the round-trip when there is nothing to compute
		if (!from_time || !to_time) return Promise.resolve(0);
		return frappe.xcall("pestcontrol.utils.calculate_duration", { from_time, to_time });
	},
};
