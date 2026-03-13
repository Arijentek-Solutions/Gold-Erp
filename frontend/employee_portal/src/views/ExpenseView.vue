<template>
	<div class="h-full flex flex-col gap-8 overflow-hidden">
		<!-- Header Section -->
		<div class="shrink-0">
			<div class="flex items-center justify-between">
				<div>
					<h2 class="premium-title">Expense Claims</h2>
					<p class="premium-subtitle">
						Manage your reimbursements and business expenses
					</p>
				</div>
				<button
					@click="showClaimModal = true"
					class="bg-primary hover:bg-yellow-400 text-black px-6 py-3 rounded-2xl font-bold flex items-center gap-2 transition-all shadow-lg shadow-primary/10"
				>
					<span class="material-symbols-outlined font-bold">add</span>
					New Claim
				</button>
			</div>

			<!-- Stats Grid -->
			<div class="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-8">
				<div class="premium-card relative group shadow-lg">
					<div
						class="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity"
					>
						<span class="material-symbols-outlined text-6xl"
							>account_balance_wallet</span
						>
					</div>
					<p class="status-label">Total Reimbursed</p>
					<div class="flex items-baseline gap-1">
						<span class="text-3xl font-bold font-mono"
							>₹{{ stats.total_reimbursed.toLocaleString() }}</span
						>
					</div>
					<div
						class="mt-4 h-1.5 w-full bg-black/5 dark:bg-white/5 rounded-full overflow-hidden"
					>
						<div class="h-full bg-emerald-500 rounded-full" style="width: 70%"></div>
					</div>
				</div>

				<div class="premium-card relative group shadow-lg">
					<div
						class="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity"
					>
						<span class="material-symbols-outlined text-6xl">pending_actions</span>
					</div>
					<p class="status-label">Pending Approval</p>
					<div class="flex items-baseline gap-1">
						<span class="text-3xl font-bold text-amber-500 font-mono"
							>₹{{ stats.pending_amount.toLocaleString() }}</span
						>
					</div>
					<p class="text-[10px] text-gray-400 dark:text-white/20 mt-4">
						{{ stats.pending_count }} claims awaiting review
					</p>
				</div>

				<div class="premium-card relative group shadow-lg">
					<div
						class="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity"
					>
						<span class="material-symbols-outlined text-6xl">receipt_long</span>
					</div>
					<p class="status-label">Monthly Limit Usage</p>
					<div class="flex items-baseline gap-1">
						<span class="text-3xl font-bold text-primary font-mono">65%</span>
					</div>
					<div
						class="mt-4 h-1.5 w-full bg-black/5 dark:bg-white/5 rounded-full overflow-hidden"
					>
						<div
							class="h-full bg-primary rounded-full transition-all duration-1000"
							style="width: 65%"
						></div>
					</div>
				</div>
			</div>
		</div>

		<!-- Claims Table Section -->
		<div class="flex-1 flex flex-col min-h-0">
			<div class="flex items-center justify-between mb-4">
				<div class="flex gap-2">
					<button
						v-for="filter in ['All', 'Pending', 'Approved', 'Rejected']"
						:key="filter"
						@click="activeFilter = filter"
						class="px-4 py-2 rounded-xl text-[10px] uppercase font-black tracking-widest transition-all"
						:class="
							activeFilter === filter
								? 'bg-primary text-black'
								: 'bg-white/5 text-white/40 hover:bg-white/10 hover:text-white'
						"
					>
						{{ filter }}
					</button>
				</div>
				<div class="text-[10px] text-white/20 uppercase tracking-widest font-bold">
					Showing {{ filteredClaims.length }} Claims
				</div>
			</div>

			<div class="flex-1 overflow-y-auto custom-scrollbar pr-2 pb-6">
				<div class="grid grid-cols-1 gap-4">
					<div
						v-if="filteredClaims.length === 0"
						class="flex flex-col items-center justify-center py-20 bg-white/[0.02] rounded-[2.5rem] border border-dashed border-white/10"
					>
						<span class="material-symbols-outlined text-6xl text-white/10 mb-4"
							>receipt_long</span
						>
						<p class="text-white/30 font-medium">
							No expense claims found matching your filter
						</p>
					</div>

					<div
						v-for="claim in filteredClaims"
						:key="claim.name"
						class="premium-card !p-6 !rounded-[1.5rem] border border-white/5 flex items-center justify-between group hover:border-white/10 transition-all"
					>
						<div class="flex items-center gap-6">
							<div
								class="w-14 h-14 rounded-2xl bg-white/5 flex items-center justify-center border border-white/10 group-hover:border-primary/30 transition-all"
							>
								<span
									class="material-symbols-outlined text-2xl"
									:class="getTypeColor(claim.expense_type)"
									>{{ getTypeIcon(claim.expense_type) }}</span
								>
							</div>
							<div>
								<h4 class="text-white font-bold text-lg mb-1">
									{{ claim.expense_type }}
								</h4>
								<div class="flex items-center gap-4">
									<p
										class="text-[10px] text-white/30 uppercase tracking-[0.1em] font-mono"
									>
										{{ formatDate(claim.posting_date) }}
									</p>
									<span class="w-1 h-1 rounded-full bg-white/10"></span>
									<p class="text-xs text-white/50">
										{{ claim.description || "No description provided" }}
									</p>
								</div>
							</div>
						</div>

						<div class="flex items-center gap-8">
							<div class="text-right">
								<p class="text-xl font-bold text-white font-mono">
									₹{{ claim.total_claimed_amount.toLocaleString() }}
								</p>
								<p
									class="text-[10px] text-white/20 uppercase tracking-[0.1em] mt-1"
								>
									{{ claim.name }}
								</p>
							</div>
							<div class="w-24 text-center">
								<span
									class="px-3 py-1.5 rounded-lg text-[9px] font-black uppercase tracking-widest inline-block w-full"
									:class="getStatusClass(claim.status)"
								>
									{{ claim.status }}
								</span>
							</div>
							<button
								class="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center text-white/30 hover:bg-white/10 hover:text-white transition-all"
							>
								<span class="material-symbols-outlined text-lg"
									>chevron_right</span
								>
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- New Claim Modal -->
		<Teleport to="body">
			<Transition name="fade">
				<div
					v-if="showClaimModal"
					class="fixed inset-0 z-[100] flex items-center justify-center p-4"
				>
					<div
						class="absolute inset-0 bg-black/80 backdrop-blur-md"
						@click="showClaimModal = false"
					></div>
					<div
						class="relative bg-white dark:bg-[#0d1017] premium-card !p-8 w-full max-w-xl shadow-[0_0_50px_rgba(0,0,0,0.5)] transform transition-all"
					>
						<div class="flex items-center justify-between mb-8">
							<h3 class="text-2xl font-bold font-display text-white">
								Submit New Claim
							</h3>
							<button
								@click="showClaimModal = false"
								class="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center text-white/40 hover:bg-white/10 hover:text-white transition-all"
							>
								<span class="material-symbols-outlined">close</span>
							</button>
						</div>

						<div class="grid grid-cols-2 gap-6">
							<div class="col-span-2">
								<label
									class="block text-[10px] text-white/30 uppercase tracking-[0.2em] font-bold mb-3 ml-1"
									>Expense Type</label
								>
								<select
									class="premium-select w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 text-white focus:outline-none focus:border-primary/50"
								>
									<option value="" disabled selected>Select category...</option>
									<option>Travel</option>
									<option>Food & Dining</option>
									<option>Office Supplies</option>
									<option>Communication</option>
									<option>Other</option>
								</select>
							</div>
							<div>
								<label
									class="block text-[10px] text-white/30 uppercase tracking-[0.2em] font-bold mb-3 ml-1"
									>Amount (₹)</label
								>
								<input
									type="number"
									placeholder="0.00"
									class="w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 text-white focus:outline-none focus:border-primary/50 font-mono"
								/>
							</div>
							<div>
								<label
									class="block text-[10px] text-white/30 uppercase tracking-[0.2em] font-bold mb-3 ml-1"
									>Date</label
								>
								<input
									type="date"
									class="w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 text-white focus:outline-none focus:border-primary/50"
								/>
							</div>
							<div class="col-span-2">
								<label
									class="block text-[10px] text-white/30 uppercase tracking-[0.2em] font-bold mb-3 ml-1"
									>Description</label
								>
								<textarea
									rows="3"
									placeholder="What was this expense for?"
									class="w-full bg-white/5 border border-white/10 rounded-2xl px-6 py-4 text-white focus:outline-none focus:border-primary/50 resize-none"
								></textarea>
							</div>
							<div class="col-span-2">
								<label
									class="block text-[10px] text-white/30 uppercase tracking-[0.2em] font-bold mb-3 ml-1"
									>Attachment (Receipt)</label
								>
								<div
									class="border-2 border-dashed border-white/10 rounded-2xl p-8 flex flex-col items-center justify-center hover:bg-white/5 hover:border-primary/30 transition-all cursor-pointer"
								>
									<span
										class="material-symbols-outlined text-3xl text-white/20 mb-2"
										>cloud_upload</span
									>
									<p class="text-xs text-white/40">
										Drop your receipt here or
										<span class="text-primary">browse</span>
									</p>
								</div>
							</div>
						</div>

						<div class="flex gap-4 mt-10">
							<button
								@click="showClaimModal = false"
								class="flex-1 py-4 bg-white/5 hover:bg-white/10 rounded-2xl text-white/60 font-bold transition-all border border-white/5"
							>
								Cancel
							</button>
							<button
								class="flex-2 py-4 bg-primary hover:bg-yellow-400 rounded-2xl text-black font-bold transition-all shadow-lg shadow-primary/10"
							>
								Submit for Approval
							</button>
						</div>
					</div>
				</div>
			</Transition>
		</Teleport>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useExpenseStore } from "@/stores/expense";
import { useEmployeeStore } from "@/stores/employee";

const expenseStore = useExpenseStore();
const employeeStore = useEmployeeStore();

const showClaimModal = ref(false);
const activeFilter = ref("All");

const stats = ref({
	total_reimbursed: 45280,
	pending_amount: 12450,
	pending_count: 3,
});

// Mock data until API is wired
const mockClaims = [
	{
		name: "EXP-2024-001",
		expense_type: "Travel",
		posting_date: "2024-03-10",
		total_claimed_amount: 5400,
		status: "Approved",
		description: "Client meeting in South Mumbai - Taxi and tolls",
	},
	{
		name: "EXP-2024-002",
		expense_type: "Food & Dining",
		posting_date: "2024-03-11",
		total_claimed_amount: 1250,
		status: "Pending",
		description: "Team lunch for project kickoff",
	},
	{
		name: "EXP-2024-003",
		expense_type: "Office Supplies",
		posting_date: "2024-03-12",
		total_claimed_amount: 850,
		status: "Draft",
		description: "Printer ink and paper reams",
	},
	{
		name: "EXP-2024-004",
		expense_type: "Communication",
		posting_date: "2024-03-05",
		total_claimed_amount: 1999,
		status: "Rejected",
		description: "Monthly broadband bill - personal usage",
	},
];

const filteredClaims = computed(() => {
	const claims = expenseStore.expenseClaims.length > 0 ? expenseStore.expenseClaims : mockClaims;
	if (activeFilter.value === "All") return claims;
	return claims.filter((c) => c.status === activeFilter.value);
});

const getTypeIcon = (type) => {
	const icons = {
		Travel: "directions_car",
		"Food & Dining": "restaurant",
		"Office Supplies": "inventory_2",
		Communication: "settings_cell",
		Other: "payments",
	};
	return icons[type] || "receipt_long";
};

const getTypeColor = (type) => {
	const colors = {
		Travel: "text-blue-400",
		"Food & Dining": "text-amber-400",
		"Office Supplies": "text-purple-400",
		Communication: "text-emerald-400",
	};
	return colors[type] || "text-white/40";
};

const getStatusClass = (status) => {
	const classes = {
		Approved: "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20",
		Pending: "bg-amber-500/10 text-amber-400 border border-amber-500/20",
		Rejected: "bg-red-500/10 text-red-400 border border-red-500/20",
		Draft: "bg-white/10 text-white/40 border border-white/20",
	};
	return classes[status] || classes["Draft"];
};

const formatDate = (dateStr) => {
	return new Date(dateStr).toLocaleDateString("en-US", {
		day: "2-digit",
		month: "short",
		year: "numeric",
	});
};

onMounted(async () => {
	await employeeStore.init();
	if (employeeStore.employee?.name) {
		expenseStore.init(employeeStore.employee.name);
	}
});
</script>

<style scoped>
.flex-2 {
	flex: 2;
}
.fade-enter-active,
.fade-leave-active {
	transition: all 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
	opacity: 0;
	transform: scale(0.95);
}
</style>
