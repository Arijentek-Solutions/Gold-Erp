import { defineStore } from "pinia";
import { createResource } from "frappe-ui";
import { ref, computed } from "vue";

export const useExpenseStore = defineStore("expense", () => {
	const expenseClaims = ref([]);
	const expenseTypes = ref([]);
	const loading = ref(false);

	// Expense Claims
	const claimsResource = createResource({
		url: "zevar_core.api.expense.get_expense_claims",
		auto: false,
		onSuccess(data) {
			expenseClaims.value = data || [];
		},
	});

	// Expense Types
	const typesResource = createResource({
		url: "zevar_core.api.expense.get_expense_types",
		auto: false,
		onSuccess(data) {
			expenseTypes.value = data || [];
		},
	});

	// Actions
	async function fetchClaims(employeeId) {
		if (!employeeId) return;
		await claimsResource.fetch({ employee: employeeId });
	}

	async function fetchTypes() {
		await typesResource.fetch();
	}

	function init(employeeId) {
		if (employeeId) {
			fetchClaims(employeeId);
			fetchTypes();
		}
	}

	return {
		expenseClaims,
		expenseTypes,
		loading,
		fetchClaims,
		fetchTypes,
		init,
	};
});
