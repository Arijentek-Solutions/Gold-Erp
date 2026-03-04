import { defineStore } from "pinia";
import { createResource } from "frappe-ui";
import { ref, computed } from "vue";

export const useAttendanceStore = defineStore("attendance", () => {
	const todayStatus = ref(null);
	const roster = ref(null);
	const history = ref([]);
	const loading = ref(false);

	// Today's check-in status
	const todayStatusResource = createResource({
		url: "zevar_core.api.attendance.get_today_checkin_status",
		auto: false,
		onSuccess(data) {
			todayStatus.value = data;
		},
	});

	// Employee roster info
	const rosterResource = createResource({
		url: "zevar_core.api.attendance.get_employee_roster",
		auto: false,
		onSuccess(data) {
			roster.value = data;
		},
	});

	// Clock in
	const clockInResource = createResource({
		url: "zevar_core.api.attendance.clock_in",
		auto: false,
	});

	// Clock out
	const clockOutResource = createResource({
		url: "zevar_core.api.attendance.clock_out",
		auto: false,
	});

	// History
	const historyResource = createResource({
		url: "zevar_core.api.attendance.get_attendance_history",
		auto: false,
		onSuccess(data) {
			history.value = data || [];
		},
	});

	// Computed
	const isCheckedIn = computed(() => {
		return todayStatus.value?.checked_in || false;
	});

	const totalHoursToday = computed(() => {
		return todayStatus.value?.total_hours_today || 0;
	});

	const overtimeHours = computed(() => {
		return todayStatus.value?.overtime_hours || 0;
	});

	const workingHoursTarget = computed(() => {
		return roster.value?.working_hours || 8;
	});

	// Actions
	async function fetchTodayStatus(employeeId) {
		if (!employeeId) return;
		await todayStatusResource.fetch({ employee_id: employeeId });
	}

	async function fetchRoster(employeeId) {
		if (!employeeId) return;
		await rosterResource.fetch({ employee_id: employeeId });
	}

	async function fetchHistory(employeeId, days = 30) {
		if (!employeeId) return;
		await historyResource.fetch({ employee_id: employeeId, days });
	}

	async function clockIn(employeeId, latitude = null, longitude = null) {
		loading.value = true;
		try {
			const result = await clockInResource.fetch({
				employee_id: employeeId,
				latitude,
				longitude,
			});
			await fetchTodayStatus(employeeId);
			return result;
		} finally {
			loading.value = false;
		}
	}

	async function clockOut(employeeId, latitude = null, longitude = null) {
		loading.value = true;
		try {
			const result = await clockOutResource.fetch({
				employee_id: employeeId,
				latitude,
				longitude,
			});
			await fetchTodayStatus(employeeId);
			return result;
		} finally {
			loading.value = false;
		}
	}

	function init(employeeId) {
		if (employeeId) {
			fetchTodayStatus(employeeId);
			fetchRoster(employeeId);
		}
	}

	return {
		todayStatus,
		roster,
		history,
		loading,
		isCheckedIn,
		totalHoursToday,
		overtimeHours,
		workingHoursTarget,
		fetchTodayStatus,
		fetchRoster,
		fetchHistory,
		clockIn,
		clockOut,
		init,
	};
});
