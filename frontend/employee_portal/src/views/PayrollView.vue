<template>
	<div class="h-full flex flex-col gap-8 overflow-hidden">
		<div class="shrink-0">
			<div class="flex items-center justify-between">
				<div>
					<h2 class="premium-title">Payroll</h2>
					<p class="premium-subtitle">View your salary slips and payroll history</p>
				</div>
				<div class="flex gap-2">
					<select
						v-model="selectedYear"
						@change="changeYear"
						class="premium-select bg-white/5 border border-white/10 rounded-xl px-4 py-2 text-white text-sm focus:outline-none focus:border-primary/50"
					>
						<option v-for="year in availableYears" :key="year" :value="year">
							{{ year }}
						</option>
					</select>
				</div>
			</div>
		</div>

		<div class="flex-1 overflow-y-auto custom-scrollbar space-y-8 pr-2">
			<!-- Summary Cards -->
			<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
				<div class="premium-card !p-6">
					<div class="flex items-center gap-3 mb-4">
						<div
							class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center border border-primary/20"
						>
							<span class="material-symbols-outlined text-primary">payments</span>
						</div>
						<span class="status-label !mb-0">Net Pay YTD</span>
					</div>
					<div class="flex items-baseline gap-2">
						<span class="text-4xl font-bold font-mono text-gray-900 dark:text-white">{{
							formatCurrency(payrollStore.totalYTD)
						}}</span>
					</div>
					<p class="premium-subtitle !text-[10px] mt-2">
						Total net pay for {{ selectedYear }}
					</p>
				</div>

				<div class="premium-card !p-6">
					<div class="flex items-center gap-3 mb-4">
						<div
							class="w-10 h-10 rounded-xl bg-emerald-500/10 flex items-center justify-center border border-emerald-500/20"
						>
							<span class="material-symbols-outlined text-emerald-500"
								>trending_up</span
							>
						</div>
						<span class="status-label !mb-0">Gross Earnings</span>
					</div>
					<div class="flex items-baseline gap-2">
						<span class="text-4xl font-bold font-mono text-gray-900 dark:text-white">{{
							formatCurrency(payrollStore.totalEarningsYTD)
						}}</span>
					</div>
					<p class="premium-subtitle !text-[10px] mt-2">
						Total earnings before deductions
					</p>
				</div>

				<div class="premium-card !p-6">
					<div class="flex items-center gap-3 mb-4">
						<div
							class="w-10 h-10 rounded-xl bg-red-400/10 flex items-center justify-center border border-red-400/20"
						>
							<span class="material-symbols-outlined text-red-400"
								>trending_down</span
							>
						</div>
						<span class="status-label !mb-0">Deductions</span>
					</div>
					<div class="flex items-baseline gap-2">
						<span class="text-4xl font-bold font-mono text-gray-900 dark:text-white">{{
							formatCurrency(payrollStore.totalDeductionsYTD)
						}}</span>
					</div>
					<p class="premium-subtitle !text-[10px] mt-2">
						Total deductions for {{ selectedYear }}
					</p>
				</div>
			</div>

			<!-- Salary Slips Table -->
			<div class="premium-card !p-0 overflow-hidden">
				<div class="p-6 border-b border-gray-100 dark:border-white/5">
					<h3 class="premium-title !text-lg">Salary Slips</h3>
				</div>

				<div v-if="payrollStore.loading" class="p-8 text-center">
					<p class="text-white/40">Loading salary slips...</p>
				</div>

				<div v-else-if="payrollStore.salarySlips.length === 0" class="p-8 text-center">
					<div
						class="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-4"
					>
						<span class="material-symbols-outlined text-3xl text-white/20"
							>receipt_long</span
						>
					</div>
					<h3 class="text-lg font-bold text-white mb-2">No Salary Slips Found</h3>
					<p class="text-white/40 text-sm">
						Your salary slips will appear here once processed by HR.
					</p>
				</div>

				<div v-else class="overflow-x-auto">
					<table class="w-full text-left">
						<thead
							class="bg-gray-50/50 dark:bg-white/5 text-[10px] text-gray-500 dark:text-white/40 uppercase font-bold tracking-wider"
						>
							<tr>
								<th class="px-6 py-4">Month</th>
								<th class="px-6 py-4">Period</th>
								<th class="px-6 py-4">Gross Pay</th>
								<th class="px-6 py-4">Deductions</th>
								<th class="px-6 py-4 text-right">Net Pay</th>
								<th class="px-6 py-4 text-right">Actions</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-white/5">
							<tr
								v-for="slip in payrollStore.salarySlips"
								:key="slip.id"
								class="group hover:bg-white/5 transition-colors"
							>
								<td class="px-6 py-4">
									<span class="font-bold text-white">{{
										slip.month || formatMonth(slip.start_date)
									}}</span>
								</td>
								<td class="px-6 py-4">
									<p class="text-white text-sm">
										{{ formatDateRange(slip.start_date, slip.end_date) }}
									</p>
								</td>
								<td class="px-6 py-4">
									<span
										class="font-bold text-emerald-600 dark:text-emerald-400 font-mono"
										>{{ formatCurrency(slip.gross_pay) }}</span
									>
								</td>
								<td class="px-6 py-4">
									<span class="text-red-500 dark:text-red-400 font-mono">{{
										formatCurrency(slip.total_deduction)
									}}</span>
								</td>
								<td class="px-6 py-4 text-right">
									<span class="text-primary font-bold font-mono text-lg">{{
										formatCurrency(slip.net_pay)
									}}</span>
								</td>
								<td class="px-6 py-4 text-right">
									<a
										:href="slip.url"
										target="_blank"
										class="text-white/40 hover:text-primary transition-colors"
									>
										<span class="material-symbols-outlined text-xl"
											>open_in_new</span
										>
									</a>
								</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>

			<!-- Latest Slip Breakdown -->
			<div v-if="payrollStore.latestSalarySlip" class="premium-card !p-0 overflow-hidden">
				<div class="p-6 border-b border-gray-100 dark:border-white/5">
					<h3 class="premium-title !text-lg">Latest Slip Breakdown</h3>
					<p class="premium-subtitle !text-xs mt-1">
						{{
							payrollStore.latestSalarySlip.month ||
							formatMonth(payrollStore.latestSalarySlip.start_date)
						}}
						{{ payrollStore.latestSalarySlip.fiscal_year }}
					</p>
				</div>

				<div
					class="grid grid-cols-1 md:grid-cols-2 divide-y md:divide-y-0 md:divide-x divide-white/5"
				>
					<!-- Earnings -->
					<div class="p-6">
						<h4 class="text-xs font-bold uppercase text-white/60 tracking-wider mb-4">
							Earnings
						</h4>
						<div class="space-y-3">
							<div
								v-for="earning in payrollStore.latestSalarySlip.earnings"
								:key="earning.component"
								class="flex justify-between items-center"
							>
								<span class="text-white/70 text-sm">{{ earning.component }}</span>
								<span class="text-white font-mono text-sm">{{
									formatCurrency(earning.amount)
								}}</span>
							</div>
							<div
								class="flex justify-between items-center pt-3 border-t border-white/10"
							>
								<span class="text-white font-bold">Total Earnings</span>
								<span class="text-emerald-glow font-bold font-mono">{{
									formatCurrency(payrollStore.latestSalarySlip.gross_pay)
								}}</span>
							</div>
						</div>
					</div>

					<!-- Deductions -->
					<div class="p-6">
						<h4 class="text-xs font-bold uppercase text-white/60 tracking-wider mb-4">
							Deductions
						</h4>
						<div class="space-y-3">
							<div
								v-for="deduction in payrollStore.latestSalarySlip.deductions"
								:key="deduction.component"
								class="flex justify-between items-center"
							>
								<span class="text-white/70 text-sm">{{
									deduction.component
								}}</span>
								<span class="text-white font-mono text-sm">{{
									formatCurrency(deduction.amount)
								}}</span>
							</div>
							<div
								class="flex justify-between items-center pt-3 border-t border-white/10"
							>
								<span class="text-white font-bold">Total Deductions</span>
								<span class="text-red-400 font-bold font-mono">{{
									formatCurrency(payrollStore.latestSalarySlip.total_deduction)
								}}</span>
							</div>
						</div>
					</div>
				</div>

				<!-- Net Pay -->
				<div class="p-6 bg-primary/5 border-t border-white/5">
					<div class="flex justify-between items-center">
						<span class="text-lg font-bold text-white">Net Pay</span>
						<span class="text-2xl font-bold text-primary font-mono">{{
							formatCurrency(payrollStore.latestSalarySlip.net_pay)
						}}</span>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { usePayrollStore } from "@/stores/payroll";
import { useEmployeeStore } from "@/stores/employee";

const payrollStore = usePayrollStore();
const employeeStore = useEmployeeStore();

const selectedYear = ref(new Date().getFullYear());
const currentYear = new Date().getFullYear();

// Available years (current year and 2 years back)
const availableYears = computed(() => {
	const years = [];
	for (let i = 0; i < 3; i++) {
		years.push(currentYear - i);
	}
	return years;
});

function changeYear() {
	payrollStore.fetchSalarySlips(selectedYear.value);
	payrollStore.fetchPayrollSummary(selectedYear.value);
}

function formatCurrency(amount) {
	if (amount === null || amount === undefined) return "₹0";
	return new Intl.NumberFormat("en-IN", {
		style: "currency",
		currency: "INR",
		minimumFractionDigits: 0,
		maximumFractionDigits: 0,
	}).format(amount);
}

function formatMonth(dateStr) {
	if (!dateStr) return "";
	const date = new Date(dateStr);
	return date.toLocaleDateString("en-US", { month: "long" });
}

function formatDateRange(start, end) {
	if (!start) return "";
	const startDate = new Date(start);
	const endDate = new Date(end);

	const startDay = startDate.getDate();
	const endDay = endDate.getDate();
	const month = endDate.toLocaleDateString("en-US", { month: "short" });
	const year = endDate.getFullYear();

	return `${startDay} - ${endDay} ${month} ${year}`;
}

onMounted(async () => {
	await employeeStore.init();
	payrollStore.init();
});
</script>
