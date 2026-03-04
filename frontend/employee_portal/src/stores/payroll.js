import { defineStore } from "pinia";
import { createResource } from "frappe-ui";
import { ref, computed } from "vue";

export const usePayrollStore = defineStore("payroll", () => {
	const salarySlips = ref([]);
	const payrollSummary = ref(null);
	const loading = ref(false);

	// Get salary slips from HRMS via zevar_core API
	const salarySlipsResource = createResource({
		url: "zevar_core.api.payroll.get_salary_slips",
		auto: false,
		onSuccess(data) {
			salarySlips.value = data || [];
		},
	});

	// Get payroll summary
	const payrollSummaryResource = createResource({
		url: "zevar_core.api.payroll.get_payroll_summary",
		auto: false,
		onSuccess(data) {
			payrollSummary.value = data;
		},
	});

	// Get salary slip details
	const salarySlipDetailsResource = createResource({
		url: "zevar_core.api.payroll.get_salary_slip_details",
		auto: false,
	});

	// Computed
	const latestSalarySlip = computed(() => {
		if (!salarySlips.value || salarySlips.value.length === 0) return null;
		return salarySlips.value[0];
	});

	const totalYTD = computed(() => {
		return payrollSummary.value?.total_net_pay || 0;
	});

	const totalEarningsYTD = computed(() => {
		return payrollSummary.value?.total_earnings || 0;
	});

	const totalDeductionsYTD = computed(() => {
		return payrollSummary.value?.total_deductions || 0;
	});

	// Actions
	async function fetchSalarySlips(year = null) {
		await salarySlipsResource.fetch({ year });
	}

	async function fetchPayrollSummary(year = null) {
		await payrollSummaryResource.fetch({ year });
	}

	async function getSlipDetails(slipName) {
		return await salarySlipDetailsResource.fetch({ slip_name: slipName });
	}

	function init() {
		fetchSalarySlips();
		fetchPayrollSummary();
	}

	return {
		salarySlips,
		payrollSummary,
		loading,
		latestSalarySlip,
		totalYTD,
		totalEarningsYTD,
		totalDeductionsYTD,
		fetchSalarySlips,
		fetchPayrollSummary,
		getSlipDetails,
		init,
	};
});
