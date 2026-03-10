import { defineStore } from "pinia";
import { createResource } from "frappe-ui";
import { ref, computed } from "vue";

export const useLeaveStore = defineStore("leave", () => {
	const leaveBalances = ref([]);
	const leaveApplications = ref([]);
	const leaveTypes = ref([]);
	const loading = ref(false);
	const employeeId = ref(null);

	// Get leave balance map from HRMS
	const leaveBalanceResource = createResource({
		url: "hrms.api.get_leave_balance_map",
		auto: false,
		onSuccess(data) {
			if (data) {
				leaveBalances.value = Object.entries(data).map(([key, value]) => ({
					leave_type: key,
					...value,
				}));
			}
		},
	});

	// Get leave applications from HRMS
	const leaveApplicationsResource = createResource({
		url: "hrms.api.get_leave_applications",
		auto: false,
		onSuccess(data) {
			leaveApplications.value = data || [];
		},
	});

	// Get leave types from HRMS
	const leaveTypesResource = createResource({
		url: "hrms.api.get_leave_types",
		auto: false,
		onSuccess(data) {
			leaveTypes.value = data || [];
		},
	});

	// Computed
	const totalLeaveBalance = computed(() => {
		return leaveBalances.value.reduce((sum, lb) => sum + (lb.balance || 0), 0);
	});

	const pendingApplications = computed(() => {
		return leaveApplications.value.filter(
			(app) => app.status === "Open" || app.status === "Pending"
		);
	});

	const approvedApplications = computed(() => {
		return leaveApplications.value.filter((app) => app.status === "Approved");
	});

	// Actions
	async function fetchLeaveBalances() {
		if (!employeeId.value) return;
		await leaveBalanceResource.fetch({ employee: employeeId.value });
	}

	async function fetchLeaveApplications() {
		if (!employeeId.value) return;
		await leaveApplicationsResource.fetch({ employee: employeeId.value });
	}

	async function fetchLeaveTypes() {
		await leaveTypesResource.fetch();
	}

	function init(empId) {
		employeeId.value = empId;
		fetchLeaveBalances();
		fetchLeaveApplications();
		fetchLeaveTypes();
	}

	return {
		leaveBalances,
		leaveApplications,
		leaveTypes,
		loading,
		totalLeaveBalance,
		pendingApplications,
		approvedApplications,
		fetchLeaveBalances,
		fetchLeaveApplications,
		fetchLeaveTypes,
		init,
	};
});
