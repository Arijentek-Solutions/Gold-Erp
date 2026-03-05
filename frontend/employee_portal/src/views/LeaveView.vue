<template>
	<div class="flex flex-col gap-8">
		<div class="flex items-center justify-between">
			<div>
				<h2 class="text-3xl font-bold font-display text-white mb-2">
					Time Off Management
				</h2>
				<p class="text-white/40">Manage your leave requests and balances</p>
			</div>
			<button
				@click="showLeaveModal = true"
				class="bg-primary text-background-dark px-6 py-3 rounded-xl font-bold flex items-center gap-2 hover:bg-yellow-400 transition-colors shadow-lg shadow-primary/20"
			>
				<span class="material-symbols-outlined">add_circle</span>
				Request Leave
			</button>
		</div>

		<!-- Balances -->
		<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
			<div v-if="leaveStore.loading" class="col-span-3 text-center py-8">
				<p class="text-white/40">Loading leave balances...</p>
			</div>

			<div v-else-if="leaveStore.leaveBalances.length === 0" class="col-span-3">
				<div class="glass-card p-8 rounded-2xl text-center">
					<div
						class="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-4"
					>
						<span class="material-symbols-outlined text-3xl text-white/20"
							>beach_access</span
						>
					</div>
					<h3 class="text-lg font-bold text-white mb-2">No Leave Balances Found</h3>
					<p class="text-white/40 text-sm">
						Your leave balances will appear here once configured in HRMS.
					</p>
				</div>
			</div>

			<template v-else>
				<div
					v-for="(balance, index) in displayedBalances"
					:key="balance.leave_type"
					class="glass-card p-6 rounded-2xl relative overflow-hidden group"
				>
					<div
						class="absolute -right-8 -top-8 text-9xl"
						:class="getBalanceColor(index).bg"
					>
						<span class="material-symbols-outlined text-[150px]">{{
							getBalanceIcon(index)
						}}</span>
					</div>
					<div class="flex items-center gap-3 mb-4">
						<span
							class="material-symbols-outlined"
							:class="getBalanceColor(index).text"
							>{{ getBalanceIcon(index) }}</span
						>
						<span class="text-xs font-bold uppercase text-white/60 tracking-wider">
							{{ balance.leave_type }}
						</span>
					</div>
					<div class="flex items-baseline gap-2 mb-2">
						<span class="text-5xl font-bold font-mono text-white">{{
							balance.balance || 0
						}}</span>
						<span class="text-white/40 text-sm">Days Available</span>
					</div>
					<div
						class="flex justify-between text-xs text-white/30 border-t border-white/5 pt-4 mt-4"
					>
						<span>Allocated: {{ balance.total_leaves || 0 }} days</span>
						<span v-if="balance.leaves_taken" class="text-primary font-bold">
							{{ balance.leaves_taken }} used
						</span>
					</div>
				</div>
			</template>
		</div>

		<!-- Leave History -->
		<div class="glass-card rounded-2xl border border-white/5 overflow-hidden">
			<div class="p-6 border-b border-white/5 flex items-center justify-between">
				<h3 class="font-bold text-lg text-white">Leave History</h3>
				<div class="flex gap-2">
					<button
						@click="filterHistory = 'all'"
						class="px-4 py-2 rounded-lg text-xs font-bold uppercase transition"
						:class="
							filterHistory === 'all'
								? 'bg-white/10 text-white'
								: 'text-white/40 hover:text-white hover:bg-white/5'
						"
					>
						All History
					</button>
					<button
						@click="filterHistory = 'pending'"
						class="px-4 py-2 rounded-lg text-xs font-bold uppercase transition"
						:class="
							filterHistory === 'pending'
								? 'bg-white/10 text-white'
								: 'text-white/40 hover:text-white hover:bg-white/5'
						"
					>
						Pending Only
					</button>
				</div>
			</div>

			<div class="overflow-x-auto">
				<table class="w-full text-left">
					<thead
						class="bg-white/5 text-xs text-white/40 uppercase font-bold tracking-wider"
					>
						<tr>
							<th class="px-6 py-4">Type</th>
							<th class="px-6 py-4">Date Range</th>
							<th class="px-6 py-4">Duration</th>
							<th class="px-6 py-4">Reason</th>
							<th class="px-6 py-4 text-right">Status</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-white/5">
						<tr v-if="filteredApplications.length === 0">
							<td colspan="5" class="px-6 py-12 text-center text-white/40">
								<div class="flex flex-col items-center gap-2">
									<span class="material-symbols-outlined text-3xl"
										>event_busy</span
									>
									<span>No leave applications found</span>
								</div>
							</td>
						</tr>
						<tr
							v-for="app in filteredApplications"
							:key="app.name"
							class="group hover:bg-white/5 transition-colors"
						>
							<td class="px-6 py-4">
								<div class="flex items-center gap-3">
									<span
										class="w-2 h-2 rounded-full"
										:class="getStatusDotColor(app.status)"
									></span>
									<span class="font-bold text-white">{{ app.leave_type }}</span>
								</div>
							</td>
							<td class="px-6 py-4">
								<p class="text-white text-sm">
									{{ formatDateRange(app.from_date, app.to_date) }}
								</p>
								<p class="text-xs text-white/30">
									{{ getDurationLabel(app.from_date, app.to_date) }}
								</p>
							</td>
							<td class="px-6 py-4">
								<span
									class="bg-white/10 px-3 py-1 rounded-full text-xs text-white font-medium"
								>
									{{ app.total_leave_days || 1 }}
									{{ (app.total_leave_days || 1) === 1 ? "Day" : "Days" }}
								</span>
							</td>
							<td class="px-6 py-4 text-white/60 text-sm italic max-w-xs truncate">
								{{ app.description || "No reason provided" }}
							</td>
							<td class="px-6 py-4 text-right">
								<span
									class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase"
									:class="getStatusStyle(app.status)"
								>
									<span
										class="w-1.5 h-1.5 rounded-full"
										:class="getStatusDotColor(app.status)"
									></span>
									{{ app.status }}
								</span>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>

		<!-- Request Leave Modal -->
		<Teleport to="body">
			<div
				v-if="showLeaveModal"
				class="fixed inset-0 z-50 flex items-center justify-center p-4"
				@click.self="showLeaveModal = false"
			>
				<div class="absolute inset-0 bg-black/60"></div>
				<div
					class="relative bg-[#111420] rounded-2xl p-6 w-full max-w-md border border-white/10"
				>
					<h3 class="font-bold text-white text-lg mb-4">Request Leave</h3>

					<div class="space-y-4">
						<div>
							<label class="block text-xs font-bold text-white/60 uppercase mb-2"
								>Leave Type</label
							>
							<select
								v-model="newLeave.leave_type"
								class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-primary/50"
							>
								<option value="" disabled>Select leave type...</option>
								<option
									v-for="lt in leaveStore.leaveTypes"
									:key="lt.name"
									:value="lt.name"
								>
									{{ lt.leave_type_name }}
								</option>
							</select>
						</div>

						<div class="grid grid-cols-2 gap-4">
							<div>
								<label class="block text-xs font-bold text-white/60 uppercase mb-2"
									>From Date</label
								>
								<input
									v-model="newLeave.from_date"
									type="date"
									class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-primary/50"
								/>
							</div>
							<div>
								<label class="block text-xs font-bold text-white/60 uppercase mb-2"
									>To Date</label
								>
								<input
									v-model="newLeave.to_date"
									type="date"
									class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-primary/50"
								/>
							</div>
						</div>

						<div>
							<label class="block text-xs font-bold text-white/60 uppercase mb-2"
								>Reason</label
							>
							<textarea
								v-model="newLeave.description"
								rows="3"
								class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-primary/50 resize-none"
								placeholder="Brief reason for leave..."
							></textarea>
						</div>
					</div>

					<div class="flex gap-3 mt-6">
						<button
							@click="showLeaveModal = false"
							class="flex-1 py-3 bg-white/5 hover:bg-white/10 rounded-xl text-white/60 text-sm font-bold transition-colors"
						>
							Cancel
						</button>
						<button
							@click="submitLeave"
							:disabled="!canSubmitLeave"
							class="flex-1 py-3 bg-primary text-black rounded-xl text-sm font-bold hover:bg-yellow-400 transition-colors disabled:opacity-50"
						>
							Submit Request
						</button>
					</div>
				</div>
			</div>
		</Teleport>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useLeaveStore } from "@/stores/leave";
import { useEmployeeStore } from "@/stores/employee";

const leaveStore = useLeaveStore();
const employeeStore = useEmployeeStore();

const showLeaveModal = ref(false);
const filterHistory = ref("all");

const newLeave = ref({
	leave_type: "",
	from_date: "",
	to_date: "",
	description: "",
});

// Display first 3 leave balances
const displayedBalances = computed(() => {
	return leaveStore.leaveBalances.slice(0, 3);
});

// Filtered applications
const filteredApplications = computed(() => {
	if (filterHistory.value === "pending") {
		return leaveStore.leaveApplications.filter(
			(app) => app.status === "Open" || app.status === "Pending"
		);
	}
	return leaveStore.leaveApplications;
});

const canSubmitLeave = computed(() => {
	return newLeave.value.leave_type && newLeave.value.from_date && newLeave.value.to_date;
});

// Helper functions
function getBalanceColor(index) {
	const colors = [
		{ bg: "text-primary/5", text: "text-primary" },
		{ bg: "text-blue-400/5", text: "text-blue-400" },
		{ bg: "text-purple-400/5", text: "text-purple-400" },
	];
	return colors[index % colors.length];
}

function getBalanceIcon(index) {
	const icons = ["flight_takeoff", "medication", "person"];
	return icons[index % icons.length];
}

function getStatusDotColor(status) {
	switch (status) {
		case "Approved":
			return "bg-emerald-glow";
		case "Open":
		case "Pending":
			return "bg-blue-400";
		case "Rejected":
			return "bg-red-400";
		default:
			return "bg-white/40";
	}
}

function getStatusStyle(status) {
	switch (status) {
		case "Approved":
			return "bg-emerald-glow/20 text-emerald-glow";
		case "Open":
		case "Pending":
			return "bg-blue-400/20 text-blue-400";
		case "Rejected":
			return "bg-red-400/20 text-red-400";
		default:
			return "bg-white/10 text-white/40";
	}
}

function formatDateRange(fromDate, toDate) {
	if (!fromDate) return "";
	const from = new Date(fromDate);
	if (!toDate || fromDate === toDate) {
		return from.toLocaleDateString("en-US", {
			month: "short",
			day: "numeric",
			year: "numeric",
		});
	}
	const to = new Date(toDate);
	return `${from.toLocaleDateString("en-US", {
		month: "short",
		day: "numeric",
	})} - ${to.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}`;
}

function getDurationLabel(fromDate, toDate) {
	if (!fromDate || !toDate) return "SINGLE DAY";
	const from = new Date(fromDate);
	const to = new Date(toDate);
	const diffTime = Math.abs(to - from);
	const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
	if (diffDays === 0) return "SINGLE DAY";
	return `${diffDays + 1} DAYS`;
}

async function submitLeave() {
	// This would call HRMS API to create leave application
	// For now, just close the modal
	showLeaveModal.value = false;
	newLeave.value = {
		leave_type: "",
		from_date: "",
		to_date: "",
		description: "",
	};
}

onMounted(async () => {
	await employeeStore.init();
	const employeeId = employeeStore.employee?.employee_id;
	if (employeeId) {
		leaveStore.init(employeeId);
	}
});
</script>
