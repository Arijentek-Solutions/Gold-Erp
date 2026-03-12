<template>
	<div class="flex flex-col gap-4 h-full overflow-hidden">
		<!-- Header Stats -->
		<div class="grid grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-4 shrink-0">
			<div class="premium-card !p-4">
				<p class="status-label">Annual Leave</p>
				<p class="text-lg sm:text-2xl font-bold font-mono text-gray-900 dark:text-white">{{ getLeaveBalance('Annual Leave') }}<span class="text-xs sm:text-sm text-gray-500 dark:text-white/40 ml-1">days</span></p>
			</div>
			<div class="premium-card !p-4">
				<p class="status-label">Sick Leave</p>
				<p class="text-lg sm:text-2xl font-bold font-mono text-gray-900 dark:text-white">{{ getLeaveBalance('Sick Leave') }}<span class="text-xs sm:text-sm text-gray-500 dark:text-white/40 ml-1">days</span></p>
			</div>
			<div class="premium-card !p-4">
				<p class="status-label">Pending</p>
				<p class="text-lg sm:text-2xl font-bold text-amber-500 dark:text-amber-400 font-mono">{{ pendingCount }}<span class="text-xs sm:text-sm text-gray-500 dark:text-white/40 ml-1">req</span></p>
			</div>
			<div class="premium-card !p-4 flex items-center justify-between">
				<div>
					<p class="status-label">Total Used</p>
					<p class="text-lg sm:text-2xl font-bold font-mono text-gray-900 dark:text-white">{{ totalUsedDays }}<span class="text-xs sm:text-sm text-gray-500 dark:text-white/40 ml-1">days</span></p>
				</div>
				<button
					@click="showLeaveModal = true"
					class="bg-primary text-black px-3 sm:px-4 py-2 rounded-xl text-[10px] sm:text-xs font-bold hover:bg-yellow-400 transition-all shadow-lg shadow-primary/20"
				>
					+ Request
				</button>
			</div>
		</div>

		<!-- Main Content -->
		<div class="flex-1 flex flex-col lg:flex-row gap-4 min-h-0 overflow-hidden">
			<!-- Leave Applications List -->
			<div class="flex-1 flex flex-col min-w-0 overflow-hidden">
				<div class="flex items-center justify-between mb-3 sm:mb-4 shrink-0">
					<div>
						<h2 class="premium-title !text-xl">Leave Applications</h2>
						<p class="premium-subtitle">Your time off requests</p>
					</div>
					<div class="flex gap-1 sm:gap-2">
						<button
							@click="filterHistory = 'all'"
							class="px-2 sm:px-3 py-1 sm:py-1.5 rounded-lg text-[9px] sm:text-[10px] font-bold uppercase transition"
							:class="filterHistory === 'all' ? 'bg-white/10 text-white' : 'text-white/40 hover:text-white'"
						>
							All
						</button>
						<button
							@click="filterHistory = 'pending'"
							class="px-2 sm:px-3 py-1 sm:py-1.5 rounded-lg text-[9px] sm:text-[10px] font-bold uppercase transition"
							:class="filterHistory === 'pending' ? 'bg-white/10 text-white' : 'text-white/40 hover:text-white'"
						>
							Pending
						</button>
						<button
							@click="filterHistory = 'approved'"
							class="hidden sm:block px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase transition"
							:class="filterHistory === 'approved' ? 'bg-white/10 text-white' : 'text-white/40 hover:text-white'"
						>
							Approved
						</button>
					</div>
				</div>

				<!-- Table Header - Hidden on mobile -->
				<div class="hidden sm:grid premium-card !p-3 !rounded-t-xl grid-cols-5 gap-2 sm:gap-4 text-[9px] sm:text-[10px] uppercase tracking-widest text-white/40 font-bold border-b border-white/5">
					<div>Leave Type</div>
					<div>Date Range</div>
					<div>Duration</div>
					<div>Reason</div>
					<div>Status</div>
				</div>

				<!-- Leave Records -->
				<div class="flex-1 overflow-y-auto custom-scrollbar">
					<div v-if="filteredApplications.length === 0" class="text-center py-12">
						<span class="material-symbols-outlined text-4xl text-white/20 mb-3">beach_access</span>
						<p class="text-white/40 text-sm">No leave applications found</p>
					</div>

					<!-- Mobile Card View -->
					<div class="sm:hidden space-y-2 p-2">
						<div
							v-for="app in filteredApplications"
							:key="app.name"
							class="premium-card !p-3 !rounded-xl border border-white/5"
						>
							<div class="flex items-center justify-between mb-2">
								<p class="text-sm font-bold text-white">{{ app.leave_type }}</p>
								<span
									class="text-[9px] px-2 py-1 rounded-full font-bold uppercase"
									:class="getStatusStyle(app.status)"
								>{{ app.status }}</span>
							</div>
							<div class="flex items-center justify-between text-[10px]">
								<span class="text-white/60">{{ formatDateShort(app.from_date) }}{{ app.to_date && app.from_date !== app.to_date ? ' - ' + formatDateShort(app.to_date) : '' }}</span>
								<span class="text-white/40">{{ app.total_leave_days || 1 }} {{ (app.total_leave_days || 1) === 1 ? 'day' : 'days' }}</span>
							</div>
							<p v-if="app.description" class="text-[10px] text-white/30 mt-2 truncate">{{ app.description }}</p>
						</div>
					</div>

					<!-- Desktop Table View -->
					<div class="hidden sm:block glass-card rounded-b-xl">
						<div
							v-for="app in filteredApplications"
							:key="app.name"
							class="grid grid-cols-5 gap-2 sm:gap-4 px-3 sm:px-4 py-2 sm:py-3 border-b border-white/5 hover:bg-white/[0.02] transition-colors items-center"
						>
							<div>
								<p class="text-xs sm:text-sm font-bold text-white">{{ app.leave_type }}</p>
							</div>
							<div>
								<p class="text-xs sm:text-sm text-white">{{ formatDateShort(app.from_date) }}</p>
								<p v-if="app.to_date && app.from_date !== app.to_date" class="text-[9px] sm:text-[10px] text-white/30">
									to {{ formatDateShort(app.to_date) }}
								</p>
							</div>
							<div>
								<span class="text-xs sm:text-sm font-mono text-white">{{ app.total_leave_days || 1 }}</span>
								<span class="text-[9px] sm:text-[10px] text-white/40 ml-1">{{ (app.total_leave_days || 1) === 1 ? 'day' : 'days' }}</span>
							</div>
							<div>
								<p class="text-[10px] sm:text-xs text-white/50 truncate max-w-[100px] sm:max-w-[150px]">{{ app.description || 'No reason provided' }}</p>
							</div>
							<div>
								<span
									class="text-[9px] sm:text-[10px] px-1.5 sm:px-2 py-0.5 sm:py-1 rounded-full font-bold uppercase"
									:class="getStatusStyle(app.status)"
								>
									{{ app.status }}
								</span>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Mini Calendar - Hidden on mobile -->
			<div class="hidden lg:block w-72 shrink-0">
				<div class="premium-card !p-4">
					<StandardCalendar 
						v-model="currentDate"
						:events="allEventDates"
					/>
				</div>

				<!-- Quick Info -->
				<div class="premium-card !p-4 mt-4">
					<h4 class="status-label !mb-3">Leave Policy</h4>
					<div class="space-y-2 text-[11px] text-gray-500 dark:text-white/40">
						<p>• Submit requests 3 days in advance</p>
						<p>• Annual leave: 21 days/year</p>
						<p>• Sick leave: 10 days/year</p>
						<p>• Contact HR for emergencies</p>
					</div>
				</div>
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
							<label class="block text-[10px] text-white/40 uppercase tracking-widest mb-2">Leave Type</label>
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
								<label class="block text-[10px] text-white/40 uppercase tracking-widest mb-2">From Date</label>
								<input
									v-model="newLeave.from_date"
									type="date"
									class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-primary/50"
								/>
							</div>
							<div>
								<label class="block text-[10px] text-white/40 uppercase tracking-widest mb-2">To Date</label>
								<input
									v-model="newLeave.to_date"
									type="date"
									class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-primary/50"
								/>
							</div>
						</div>

						<div>
							<label class="block text-[10px] text-white/40 uppercase tracking-widest mb-2">Reason</label>
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
import StandardCalendar from "@/components/StandardCalendar.vue";

const leaveStore = useLeaveStore();
const employeeStore = useEmployeeStore();

const showLeaveModal = ref(false);
const filterHistory = ref("all");
const currentDate = ref(new Date());

const newLeave = ref({
	leave_type: "",
	from_date: "",
	to_date: "",
	description: "",
});

// Current month display
const currentMonthYear = computed(() => {
	return currentDate.value.toLocaleDateString("en-US", { month: "long", year: "numeric" });
});

// Get first day of month (0 = Sunday, 1 = Monday, etc.)
const firstDayOfMonth = computed(() => {
	const firstDay = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth(), 1);
	const day = firstDay.getDay();
	return day === 0 ? 6 : day - 1;
});

// Get days in month
const daysInMonth = computed(() => {
	return new Date(
		currentDate.value.getFullYear(),
		currentDate.value.getMonth() + 1,
		0
	).getDate();
});

const allEventDates = computed(() => {
	const dates = [];
	leaveStore.leaveApplications.forEach(app => {
		const start = new Date(app.from_date);
		const end = new Date(app.to_date || app.from_date);
		for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
			dates.push(new Date(d));
		}
	});
	return dates;
});

// Get leave dates for calendar
const leaveDates = computed(() => {
	const dates = new Set();
	leaveStore.leaveApplications
		.filter(app => app.status === 'Approved')
		.forEach(app => {
			const start = new Date(app.from_date);
			const end = new Date(app.to_date || app.from_date);
			for (let d = start; d <= end; d.setDate(d.getDate() + 1)) {
				dates.add(d.toISOString().split('T')[0]);
			}
		});
	return dates;
});

const pendingDates = computed(() => {
	const dates = new Set();
	leaveStore.leaveApplications
		.filter(app => app.status === 'Open' || app.status === 'Pending')
		.forEach(app => {
			const start = new Date(app.from_date);
			const end = new Date(app.to_date || app.from_date);
			for (let d = start; d <= end; d.setDate(d.getDate() + 1)) {
				dates.add(d.toISOString().split('T')[0]);
			}
		});
	return dates;
});

// Calendar days
const calendarDays = computed(() => {
	const today = new Date();
	const days = [];

	for (let i = 1; i <= daysInMonth.value; i++) {
		const dayDate = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth(), i);
		const dateStr = dayDate.toISOString().split('T')[0];
		const isToday =
			dayDate.getDate() === today.getDate() &&
			dayDate.getMonth() === today.getMonth() &&
			dayDate.getFullYear() === today.getFullYear();

		const dayOfWeek = dayDate.getDay();
		const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;

		days.push({
			day: i,
			date: dateStr,
			isToday,
			isWeekend,
			hasLeave: leaveDates.value.has(dateStr),
			hasPending: pendingDates.value.has(dateStr),
		});
	}

	return days;
});

// Stats
const pendingCount = computed(() => {
	return leaveStore.leaveApplications.filter(
		app => app.status === 'Open' || app.status === 'Pending'
	).length;
});

const totalUsedDays = computed(() => {
	return leaveStore.leaveApplications
		.filter(app => app.status === 'Approved')
		.reduce((sum, app) => sum + (app.total_leave_days || 1), 0);
});

// Filtered applications
const filteredApplications = computed(() => {
	let apps = leaveStore.leaveApplications;
	if (filterHistory.value === 'pending') {
		apps = apps.filter(app => app.status === 'Open' || app.status === 'Pending');
	} else if (filterHistory.value === 'approved') {
		apps = apps.filter(app => app.status === 'Approved');
	}
	return apps.sort((a, b) => new Date(b.from_date) - new Date(a.from_date));
});

const canSubmitLeave = computed(() => {
	return newLeave.value.leave_type && newLeave.value.from_date && newLeave.value.to_date;
});

// Helper functions
function getLeaveBalance(type) {
	const balance = leaveStore.leaveBalances.find(b => b.leave_type === type);
	return balance?.balance || 0;
}

function getStatusStyle(status) {
	switch (status) {
		case "Approved":
			return "bg-emerald-500/15 text-emerald-400";
		case "Open":
		case "Pending":
			return "bg-amber-500/15 text-amber-400";
		case "Rejected":
			return "bg-red-500/15 text-red-400";
		default:
			return "bg-white/10 text-white/40";
	}
}

function formatDateShort(dateStr) {
	if (!dateStr) return "";
	const date = new Date(dateStr);
	return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function previousMonth() {
	currentDate.value = new Date(
		currentDate.value.getFullYear(),
		currentDate.value.getMonth() - 1,
		1
	);
}

function nextMonth() {
	currentDate.value = new Date(
		currentDate.value.getFullYear(),
		currentDate.value.getMonth() + 1,
		1
	);
}

async function submitLeave() {
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
	const employeeId = employeeStore.employee?.name;
	if (employeeId) {
		leaveStore.init(employeeId);
	}
});
</script>
