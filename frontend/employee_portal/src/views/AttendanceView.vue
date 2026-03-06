<template>
	<div class="flex flex-col gap-4 h-full overflow-hidden">
		<!-- Header Stats -->
		<div class="grid grid-cols-3 sm:grid-cols-3 gap-2 sm:gap-4 shrink-0">
			<div class="glass-card p-3 sm:p-4 rounded-xl">
				<p class="text-[9px] sm:text-[10px] text-white/40 uppercase tracking-widest mb-1">This Month</p>
				<p class="text-lg sm:text-2xl font-bold text-white font-mono">{{ totalHours.toFixed(1) }}<span class="text-xs sm:text-sm text-white/40 ml-1">hrs</span></p>
			</div>
			<div class="glass-card p-3 sm:p-4 rounded-xl">
				<p class="text-[9px] sm:text-[10px] text-white/40 uppercase tracking-widest mb-1">On-Time</p>
				<p class="text-lg sm:text-2xl font-bold text-white font-mono">{{ onTimeRate }}<span class="text-xs sm:text-sm text-white/40 ml-1">%</span></p>
			</div>
			<div class="glass-card p-3 sm:p-4 rounded-xl">
				<p class="text-[9px] sm:text-[10px] text-white/40 uppercase tracking-widest mb-1">Avg Shift</p>
				<p class="text-lg sm:text-2xl font-bold text-white font-mono">{{ averageShiftHours }}<span class="text-xs sm:text-sm text-white/40 ml-1">hrs</span></p>
			</div>
		</div>

		<!-- Main Content - Responsive Layout -->
		<div class="flex-1 flex flex-col lg:flex-row gap-4 min-h-0 overflow-hidden">
			<!-- Daily Attendance List -->
			<div class="flex-1 flex flex-col min-w-0 overflow-hidden">
				<div class="flex items-center justify-between mb-3 sm:mb-4 shrink-0">
					<div>
						<h2 class="text-base sm:text-xl font-bold text-white">Daily Attendance</h2>
						<p class="text-[10px] sm:text-xs text-white/40">Your clock in/out history</p>
					</div>
					<button
						@click="loadMoreHistory"
						class="text-[10px] sm:text-xs text-primary hover:text-yellow-400 font-bold transition-colors"
					>
						Load More
					</button>
				</div>

				<!-- Table Header - Hidden on mobile -->
				<div class="hidden sm:grid glass-card rounded-t-xl px-3 sm:px-4 py-2 sm:py-3 grid-cols-5 gap-2 sm:gap-4 text-[9px] sm:text-[10px] uppercase tracking-widest text-white/40 font-bold border-b border-white/5">
					<div>Date</div>
					<div>Clock In</div>
					<div>Clock Out</div>
					<div>Hours</div>
					<div>Status</div>
				</div>

				<!-- Daily Records -->
				<div class="flex-1 overflow-y-auto custom-scrollbar">
					<div v-if="dailyRecords.length === 0" class="text-center py-12">
						<span class="material-symbols-outlined text-4xl text-white/20 mb-3">event_busy</span>
						<p class="text-white/40 text-sm">No attendance records found</p>
					</div>

					<!-- Mobile Card View -->
					<div class="sm:hidden space-y-2 p-2">
						<div
							v-for="record in dailyRecords"
							:key="record.date"
							class="glass-card rounded-xl p-3 border border-white/5"
						>
							<div class="flex items-center justify-between mb-2">
								<div>
									<p class="text-sm font-bold text-white">{{ formatDate(record.date) }}</p>
									<p class="text-[10px] text-white/30">{{ formatDay(record.date) }}</p>
								</div>
								<span
									v-if="record.status === 'present'"
									class="text-[9px] px-2 py-1 rounded-full bg-emerald-500/15 text-emerald-400 font-bold uppercase"
								>Present</span>
								<span
									v-else-if="record.status === 'late'"
									class="text-[9px] px-2 py-1 rounded-full bg-amber-500/15 text-amber-400 font-bold uppercase"
								>Late</span>
								<span
									v-else-if="record.status === 'absent'"
									class="text-[9px] px-2 py-1 rounded-full bg-red-500/15 text-red-400 font-bold uppercase"
								>Absent</span>
								<span
									v-else-if="record.status === 'weekend'"
									class="text-[9px] px-2 py-1 rounded-full bg-white/5 text-white/30 font-bold uppercase"
								>Off</span>
								<span v-else class="text-[9px] text-white/20">—</span>
							</div>
							<div class="grid grid-cols-3 gap-2 text-center">
								<div>
									<p class="text-[9px] text-white/30 uppercase">In</p>
									<p class="text-xs font-mono text-emerald-400">{{ record.clockIn ? formatTime(record.clockIn) : '—' }}</p>
								</div>
								<div>
									<p class="text-[9px] text-white/30 uppercase">Out</p>
									<p class="text-xs font-mono text-blue-400">{{ record.clockOut ? formatTime(record.clockOut) : '—' }}</p>
								</div>
								<div>
									<p class="text-[9px] text-white/30 uppercase">Hours</p>
									<p class="text-xs font-mono text-white">{{ record.totalHours ? record.totalHours.toFixed(1) : '—' }}</p>
								</div>
							</div>
						</div>
					</div>

					<!-- Desktop Table View -->
					<div class="hidden sm:block">
						<div
							v-for="record in dailyRecords"
							:key="record.date"
							class="grid grid-cols-5 gap-2 sm:gap-4 px-3 sm:px-4 py-2 sm:py-3 border-b border-white/5 hover:bg-white/[0.02] transition-colors items-center"
						>
							<div>
								<p class="text-xs sm:text-sm font-bold text-white">{{ formatDate(record.date) }}</p>
								<p class="text-[9px] sm:text-[10px] text-white/30">{{ formatDay(record.date) }}</p>
							</div>
							<div>
								<p v-if="record.clockIn" class="text-xs sm:text-sm font-mono text-emerald-400">
									{{ formatTime(record.clockIn) }}
								</p>
								<p v-else class="text-xs sm:text-sm text-white/20">—</p>
							</div>
							<div>
								<p v-if="record.clockOut" class="text-xs sm:text-sm font-mono text-blue-400">
									{{ formatTime(record.clockOut) }}
								</p>
								<p v-else class="text-xs sm:text-sm text-white/20">—</p>
							</div>
							<div>
								<p v-if="record.totalHours" class="text-xs sm:text-sm font-mono text-white">
									{{ record.totalHours.toFixed(2) }}
								</p>
								<p v-else class="text-xs sm:text-sm text-white/20">—</p>
							</div>
							<div>
								<span
									v-if="record.status === 'present'"
									class="text-[9px] sm:text-[10px] px-1.5 sm:px-2 py-0.5 sm:py-1 rounded-full bg-emerald-500/15 text-emerald-400 font-bold uppercase"
								>Present</span>
								<span
									v-else-if="record.status === 'late'"
									class="text-[9px] sm:text-[10px] px-1.5 sm:px-2 py-0.5 sm:py-1 rounded-full bg-amber-500/15 text-amber-400 font-bold uppercase"
								>Late</span>
								<span
									v-else-if="record.status === 'absent'"
									class="text-[9px] sm:text-[10px] px-1.5 sm:px-2 py-0.5 sm:py-1 rounded-full bg-red-500/15 text-red-400 font-bold uppercase"
								>Absent</span>
								<span
									v-else-if="record.status === 'weekend'"
									class="text-[9px] sm:text-[10px] px-1.5 sm:px-2 py-0.5 sm:py-1 rounded-full bg-white/5 text-white/30 font-bold uppercase"
								>Off</span>
								<span
									v-else-if="record.status === 'leave'"
									class="text-[9px] sm:text-[10px] px-1.5 sm:px-2 py-0.5 sm:py-1 rounded-full bg-blue-500/15 text-blue-400 font-bold uppercase"
								>Leave</span>
								<span v-else class="text-[9px] sm:text-[10px] text-white/20">—</span>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Mini Calendar - Hidden on mobile, shows below on tablet -->
			<div class="hidden lg:block w-72 shrink-0">
				<div class="glass-card rounded-xl p-4 border border-white/5">
					<!-- Calendar Header -->
					<div class="flex items-center justify-between mb-4">
						<h3 class="text-sm font-bold text-white">{{ currentMonthYear }}</h3>
						<div class="flex gap-1">
							<button
								@click="previousMonth"
								class="p-1 rounded hover:bg-white/5 text-white/40 hover:text-white transition-colors"
							>
								<span class="material-symbols-outlined text-lg">chevron_left</span>
							</button>
							<button
								@click="nextMonth"
								class="p-1 rounded hover:bg-white/5 text-white/40 hover:text-white transition-colors"
							>
								<span class="material-symbols-outlined text-lg">chevron_right</span>
							</button>
						</div>
					</div>

					<!-- Day Headers -->
					<div class="grid grid-cols-7 gap-1 mb-2">
						<div class="text-[9px] text-center text-white/30 font-bold uppercase">M</div>
						<div class="text-[9px] text-center text-white/30 font-bold uppercase">T</div>
						<div class="text-[9px] text-center text-white/30 font-bold uppercase">W</div>
						<div class="text-[9px] text-center text-white/30 font-bold uppercase">T</div>
						<div class="text-[9px] text-center text-white/30 font-bold uppercase">F</div>
						<div class="text-[9px] text-center text-white/30 font-bold uppercase">S</div>
						<div class="text-[9px] text-center text-white/30 font-bold uppercase">S</div>
					</div>

					<!-- Calendar Grid -->
					<div class="grid grid-cols-7 gap-1">
						<!-- Empty cells for days before month start -->
						<div v-for="i in firstDayOfMonth" :key="'empty-' + i" class="aspect-square"></div>

						<!-- Days -->
						<button
							v-for="day in calendarDays"
							:key="day.date"
							class="aspect-square rounded-md flex items-center justify-center text-xs relative transition-all"
							:class="[
								day.isToday
									? 'bg-primary/20 text-primary font-bold'
									: day.status === 'present'
									? 'text-emerald-400'
									: day.status === 'absent'
									? 'text-red-400'
									: day.status === 'weekend'
									? 'text-white/20'
									: 'text-white/50 hover:bg-white/5'
							]"
						>
							{{ day.day }}
							<span
								v-if="day.status === 'present' && !day.isToday"
								class="absolute bottom-0.5 w-1 h-1 rounded-full bg-emerald-400"
							></span>
							<span
								v-if="day.status === 'absent'"
								class="absolute bottom-0.5 w-1 h-1 rounded-full bg-red-400"
							></span>
						</button>
					</div>

					<!-- Legend -->
					<div class="mt-4 pt-3 border-t border-white/5 flex flex-wrap gap-3 text-[9px]">
						<div class="flex items-center gap-1">
							<span class="w-2 h-2 rounded-full bg-emerald-400"></span>
							<span class="text-white/40">Present</span>
						</div>
						<div class="flex items-center gap-1">
							<span class="w-2 h-2 rounded-full bg-red-400"></span>
							<span class="text-white/40">Absent</span>
						</div>
						<div class="flex items-center gap-1">
							<span class="w-2 h-2 rounded-full bg-primary"></span>
							<span class="text-white/40">Today</span>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useEmployeeStore } from "@/stores/employee";
import { useAttendanceStore } from "@/stores/attendance";

const employeeStore = useEmployeeStore();
const attendanceStore = useAttendanceStore();

const currentDate = ref(new Date());
const historyDays = ref(30);

// Current month display
const currentMonthYear = computed(() => {
	return currentDate.value.toLocaleDateString("en-US", { month: "short", year: "numeric" });
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

// Calendar days
const calendarDays = computed(() => {
	const today = new Date();
	const days = [];

	for (let i = 1; i <= daysInMonth.value; i++) {
		const dayDate = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth(), i);
		const isToday =
			dayDate.getDate() === today.getDate() &&
			dayDate.getMonth() === today.getMonth() &&
			dayDate.getFullYear() === today.getFullYear();

		const status = getDayStatus(dayDate);

		days.push({
			day: i,
			date: dayDate.toISOString().split("T")[0],
			isToday,
			status,
		});
	}

	return days;
});

// Daily records from history
const dailyRecords = computed(() => {
	const records = [];
	const history = attendanceStore.history || [];

	// Group logs by date
	const logsByDate = {};
	history.forEach(log => {
		if (!log.time) return;
		const dateStr = log.time.split('T')[0];
		if (!logsByDate[dateStr]) {
			logsByDate[dateStr] = { logs: [], date: dateStr };
		}
		logsByDate[dateStr].logs.push(log);
	});

	// Convert to array and process
	Object.values(logsByDate).forEach(dayData => {
		const date = new Date(dayData.date);
		const dayOfWeek = date.getDay();
		const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;

		// Find first IN and last OUT
		const inLogs = dayData.logs.filter(l => l.log_type === 'IN');
		const outLogs = dayData.logs.filter(l => l.log_type === 'OUT');

		const clockIn = inLogs.length > 0 ? inLogs[0].time : null;
		const clockOut = outLogs.length > 0 ? outLogs[outLogs.length - 1].time : null;

		// Calculate total hours
		let totalHours = 0;
		if (clockIn && clockOut) {
			const inTime = new Date(clockIn);
			const outTime = new Date(clockOut);
			totalHours = (outTime - inTime) / (1000 * 60 * 60);
		}

		// Determine status
		let status = '';
		if (isWeekend) {
			status = 'weekend';
		} else if (clockIn) {
			// Check if late (after 9 AM or configured start time)
			const inTime = new Date(clockIn);
			const lateThreshold = new Date(date);
			lateThreshold.setHours(9, 0, 0);
			status = inTime > lateThreshold ? 'late' : 'present';
		} else {
			const today = new Date();
			if (date < today) {
				status = 'absent';
			}
		}

		records.push({
			date: dayData.date,
			clockIn,
			clockOut,
			totalHours,
			status
		});
	});

	// Sort by date descending
	records.sort((a, b) => new Date(b.date) - new Date(a.date));

	return records;
});

// Stats
const totalHours = computed(() => {
	return dailyRecords.value.reduce((sum, r) => sum + (r.totalHours || 0), 0);
});

const onTimeRate = computed(() => {
	const present = dailyRecords.value.filter(r => r.status === 'present' || r.status === 'late');
	const onTime = present.filter(r => r.status === 'present');
	return present.length > 0 ? Math.round((onTime.length / present.length) * 100) : 100;
});

const averageShiftHours = computed(() => {
	const withHours = dailyRecords.value.filter(r => r.totalHours > 0);
	if (withHours.length === 0) return 0;
	const total = withHours.reduce((sum, r) => sum + r.totalHours, 0);
	return (total / withHours.length).toFixed(1);
});

// Methods
function getDayStatus(date) {
	const dayOfWeek = date.getDay();
	if (dayOfWeek === 0 || dayOfWeek === 6) {
		return "weekend";
	}

	const dateStr = date.toISOString().split("T")[0];
	const logs = attendanceStore.history.filter((log) => log.time && log.time.startsWith(dateStr));

	if (logs.length > 0) {
		return "present";
	}

	const today = new Date();
	if (date > today) {
		return "";
	}

	return "absent";
}

function formatDate(dateStr) {
	if (!dateStr) return "";
	const date = new Date(dateStr);
	return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function formatDay(dateStr) {
	if (!dateStr) return "";
	const date = new Date(dateStr);
	return date.toLocaleDateString("en-US", { weekday: "short" });
}

function formatTime(timeStr) {
	if (!timeStr) return "";
	const date = new Date(timeStr);
	return date.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit", hour12: true });
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

async function loadMoreHistory() {
	historyDays.value += 30;
	const employeeId = employeeStore.employee?.name;
	if (employeeId) {
		await attendanceStore.fetchHistory(employeeId, historyDays.value);
	}
}

// Initialize
onMounted(async () => {
	await employeeStore.init();
	const employeeId = employeeStore.employee?.name;
	if (employeeId) {
		attendanceStore.init(employeeId);
		await attendanceStore.fetchHistory(employeeId, historyDays.value);
	}
});
</script>
