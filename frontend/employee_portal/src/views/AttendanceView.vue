<template>
	<div class="flex flex-col gap-6 h-full overflow-hidden">
		<!-- Clock In/Out Section with Live Timer -->
		<div class="shrink-0">
			<div class="premium-card !p-4 sm:!p-6">
				<div class="flex flex-col sm:flex-row items-center gap-4 sm:gap-6">
					<!-- Live Timer Display -->
					<div class="flex-shrink-0 text-center">
						<div
							class="w-28 h-28 sm:w-36 sm:h-36 rounded-full flex items-center justify-center"
							:class="timerCircleClass"
						>
							<div class="text-center">
								<p
									class="text-xl sm:text-2xl font-mono font-bold"
									:class="timerTextClass"
								>
									{{ formattedTimer }}
								</p>
								<p
									class="text-[8px] sm:text-[10px] text-white/40 uppercase tracking-widest mt-1"
								>
									{{ timerLabel }}
								</p>
							</div>
						</div>
					</div>

					<!-- Timer Info & Controls -->
					<div class="flex-1 text-center sm:text-left">
						<!-- Status Badge -->
						<div class="flex items-center justify-center sm:justify-start gap-2 mb-3">
							<span
								v-if="isOnBreak"
								class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-bold uppercase bg-sky-500/15 text-sky-400"
							>
								<span class="w-1.5 h-1.5 rounded-full bg-sky-400"></span>
								On Break
							</span>
							<span
								v-else-if="isCheckedIn"
								class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-bold uppercase"
								:class="
									shiftComplete
										? 'bg-emerald-500/15 text-emerald-400'
										: 'bg-amber-500/15 text-amber-400'
								"
							>
								<span
									class="w-1.5 h-1.5 rounded-full"
									:class="shiftComplete ? 'bg-emerald-400' : 'bg-amber-400'"
								></span>
								{{ shiftComplete ? "Complete" : "Active" }}
							</span>
							<span
								v-else-if="hasWorkedToday"
								class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/5 text-white/60 text-[10px] font-bold uppercase"
							>
								<span class="w-1.5 h-1.5 rounded-full bg-white/30"></span>
								Clocked Out
							</span>
							<span
								v-else
								class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/5 text-white/40 text-[10px] font-bold uppercase"
							>
								<span class="w-1.5 h-1.5 rounded-full bg-white/30"></span>
								Not Clocked In
							</span>
						</div>

						<!-- Target Hours -->
						<p class="text-xs sm:text-sm text-white/50 mb-4">
							Target:
							<span class="font-bold text-white">{{ workingHoursTarget }} hrs</span>
							<span v-if="roster?.shift_name" class="text-white/30 ml-2"
								>({{ roster.shift_name }})</span
							>
						</p>

						<!-- Today's Summary -->
						<div
							v-if="totalHoursToday > 0"
							class="mt-4 flex items-center justify-center sm:justify-start gap-4"
						>
							<div>
								<p class="status-label !mb-0 text-[10px]">Today</p>
								<p
									class="font-mono font-bold text-gray-900 dark:text-white text-sm"
								>
									{{ totalHoursToday.toFixed(2) }} hrs
								</p>
							</div>
							<div v-if="overtimeHours > 0">
								<p
									class="status-label !mb-0 text-[10px] text-emerald-600 dark:text-emerald-400"
								>
									Overtime
								</p>
								<p
									class="font-mono font-bold text-emerald-600 dark:text-emerald-400 text-sm"
								>
									+{{ overtimeHours.toFixed(2) }} hrs
								</p>
							</div>
						</div>

						<!-- Quick Actions -->
						<div class="mt-6 grid grid-cols-2 gap-2 w-full max-w-sm">
							<button
								@click="handleClockIn"
								:disabled="isCheckedIn || isOnBreak || attendanceStore.loading"
								class="h-11 rounded-xl flex items-center justify-center gap-2 font-bold text-[10px] uppercase transition-all shadow-lg"
								:class="[
									!isCheckedIn && !isOnBreak
										? 'bg-primary text-black hover:bg-yellow-400 shadow-primary/20'
										: 'bg-white/5 border border-white/10 text-white/20 cursor-not-allowed dark:disabled:text-white/10',
								]"
							>
								Clock In
							</button>
							<button
								@click="handleClockOut"
								:disabled="!isCheckedIn || attendanceStore.loading"
								class="h-11 rounded-xl flex items-center justify-center gap-2 font-bold text-[10px] uppercase transition-all shadow-lg"
								:class="[
									isCheckedIn
										? 'bg-red-500/20 border border-red-500/30 text-red-500 hover:bg-red-500/30 shadow-red-500/10'
										: 'bg-white/5 border border-white/10 text-white/20 cursor-not-allowed dark:disabled:text-white/10',
								]"
							>
								Clock Out
							</button>
							<button
								@click="handleBreak"
								:disabled="!canManageBreak || attendanceStore.loading"
								class="col-span-2 h-11 rounded-xl flex items-center justify-center gap-2 font-bold text-[10px] uppercase transition-colors"
								:class="
									isOnBreak
										? 'bg-primary text-black shadow-primary/20'
										: 'bg-white/5 border border-white/10 text-white/80 hover:bg-white/10 disabled:opacity-30 dark:disabled:text-white/10'
								"
							>
								<span v-if="attendanceStore.loading" class="text-sm">...</span>
								<span v-else>{{ isOnBreak ? "End Break" : "Break" }}</span>
							</button>
						</div>
					</div>

					<!-- Shift Info (Desktop) -->
					<div class="hidden lg:block text-right shrink-0">
						<p class="text-[9px] text-white/30 uppercase tracking-widest mb-2">
							Shift
						</p>
						<p class="text-sm font-bold text-white">
							{{ roster?.start_time ? formatTime(roster.start_time) : "09:00" }}
							-
							{{ roster?.end_time ? formatTime(roster.end_time) : "17:00" }}
						</p>
						<p class="text-[10px] text-white/40 mt-1">
							{{ roster?.employment_type || "Full-time" }}
						</p>
					</div>
				</div>
			</div>
		</div>

		<!-- Header Stats -->
		<div class="grid grid-cols-3 gap-2 sm:gap-4 shrink-0">
			<div class="premium-card !p-3 sm:!p-4">
				<p class="status-label !mb-1">This Month</p>
				<p class="text-lg sm:text-2xl font-bold text-gray-900 dark:text-white font-mono">
					{{ totalHours.toFixed(1)
					}}<span class="text-xs sm:text-sm text-gray-400 dark:text-white/40 ml-1"
						>hrs</span
					>
				</p>
			</div>
			<div class="premium-card !p-3 sm:!p-4">
				<p class="status-label !mb-1">On-Time</p>
				<p
					class="text-lg sm:text-2xl font-bold text-emerald-600 dark:text-emerald-400 font-mono"
				>
					{{ onTimeRate
					}}<span class="text-xs sm:text-sm text-gray-400 dark:text-white/40 ml-1"
						>%</span
					>
				</p>
			</div>
			<div class="premium-card !p-3 sm:!p-4">
				<p class="status-label !mb-1">Avg Shift</p>
				<p class="text-lg sm:text-2xl font-bold text-primary font-mono">
					{{ averageShiftHours
					}}<span class="text-xs sm:text-sm text-gray-400 dark:text-white/40 ml-1"
						>hrs</span
					>
				</p>
			</div>
		</div>

		<!-- Main Content - Responsive Layout -->
		<div class="flex-1 flex flex-col lg:flex-row gap-4 min-h-0 overflow-hidden">
			<!-- Daily Attendance List -->
			<div class="flex-1 flex flex-col min-w-0 overflow-hidden">
				<div class="flex items-center justify-between mb-3 sm:mb-4 shrink-0">
					<div>
						<h2 class="premium-title !text-xl">Daily Attendance</h2>
						<p class="premium-subtitle !text-xs">Your clock in/out history</p>
					</div>
					<button
						@click="loadMoreHistory"
						class="text-[10px] sm:text-xs text-primary hover:text-yellow-400 font-bold transition-colors"
					>
						Load More
					</button>
				</div>

				<!-- Unified Table Container -->
				<div
					class="flex-1 flex flex-col premium-card !p-0 border border-white/10 overflow-hidden shadow-2xl"
				>
					<!-- Table Header -->
					<div
						class="hidden sm:grid grid-cols-5 gap-4 px-6 py-5 text-[12px] sm:text-[13px] uppercase tracking-[0.3em] font-black border-b border-white/10 attendance-header-shiny z-10 sticky top-0 backdrop-blur-md text-vibrant-emerald"
					>
						<div class="drop-shadow-md">Date</div>
						<div class="drop-shadow-md">Clock In</div>
						<div class="drop-shadow-md">Clock Out</div>
						<div class="drop-shadow-md">Hours</div>
						<div class="drop-shadow-md">Status</div>
					</div>

					<!-- Scrollable Records -->
					<div class="flex-1 overflow-y-auto custom-scrollbar">
						<!-- Empty State -->
						<div v-if="dailyRecords.length === 0" class="!p-16 text-center">
							<span class="material-symbols-outlined text-5xl text-white/10 mb-4"
								>event_busy</span
							>
							<p class="premium-subtitle !text-white/60">
								No attendance records found
							</p>
						</div>

						<!-- Mobile Card View (Visible only on mobile) -->
						<div class="sm:hidden space-y-3 p-3">
							<div
								v-for="record in dailyRecords"
								:key="record.date"
								class="premium-card !p-4 border border-white/10 bg-white/[0.02]"
							>
								<div class="flex items-center justify-between mb-3">
									<div>
										<p class="text-sm font-black text-white">
											{{ formatDate(record.date) }}
										</p>
										<p class="status-label !mb-0 !text-[10px] !text-white/70">
											{{ formatDay(record.date) }}
										</p>
									</div>
									<div class="scale-90 origin-right">
										<span
											v-if="record.status === 'complete'"
											class="text-[9px] px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-bold uppercase"
											>Complete</span
										>
										<span
											v-else-if="record.status === 'present'"
											class="text-[9px] px-2 py-1 rounded-full bg-emerald-500/15 text-emerald-400 font-bold uppercase"
											>Present</span
										>
										<span
											v-else-if="record.status === 'late'"
											class="text-[9px] px-2 py-1 rounded-full bg-amber-500/15 text-amber-400 font-bold uppercase"
											>Late</span
										>
										<span
											v-else-if="record.status === 'absent'"
											class="text-[9px] px-2 py-1 rounded-full bg-red-500/15 text-red-400 font-bold uppercase"
											>Absent</span
										>
										<span v-else class="text-[9px] text-white/30">-</span>
									</div>
								</div>
								<div
									class="grid grid-cols-3 gap-2 border-t border-white/5 pt-3 mt-3"
								>
									<div class="text-center">
										<p class="text-[9px] text-white/30 uppercase mb-1">In</p>
										<p class="text-xs font-mono text-emerald-400 font-bold">
											{{ record.clockIn ? formatTime(record.clockIn) : "-" }}
										</p>
									</div>
									<div class="text-center">
										<p class="text-[9px] text-white/30 uppercase mb-1">Out</p>
										<p class="text-xs font-mono text-blue-400 font-bold">
											{{
												record.clockOut ? formatTime(record.clockOut) : "-"
											}}
										</p>
									</div>
									<div class="text-center">
										<p class="text-[9px] text-white/30 uppercase mb-1">
											Hours
										</p>
										<p
											class="text-xs font-mono font-bold"
											:class="
												record.totalHours >= workingHoursTarget
													? 'text-emerald-400'
													: 'text-white'
											"
										>
											{{
												record.totalHours
													? record.totalHours.toFixed(1)
													: "-"
											}}
										</p>
									</div>
								</div>
							</div>
						</div>

						<!-- Desktop Table View (Visible only on desktop) -->
						<div class="hidden sm:block">
							<div
								v-for="record in dailyRecords"
								:key="record.date"
								class="grid grid-cols-5 gap-4 px-6 py-4 border-b border-white/5 hover:bg-white/[0.04] transition-all duration-200 items-center"
							>
								<div>
									<p class="text-sm sm:text-base font-black text-white mb-0.5">
										{{ formatDate(record.date) }}
									</p>
									<p
										class="text-[11px] sm:text-[12px] text-white/80 tracking-widest font-bold"
									>
										{{ formatDay(record.date) }}
									</p>
								</div>
								<div>
									<p
										v-if="record.clockIn"
										class="text-sm font-mono text-emerald-400 font-bold"
									>
										{{ formatTime(record.clockIn) }}
									</p>
									<p v-else class="text-sm text-white/20">-</p>
								</div>
								<div>
									<p
										v-if="record.clockOut"
										class="text-sm font-mono text-blue-400 font-bold"
									>
										{{ formatTime(record.clockOut) }}
									</p>
									<p v-else class="text-sm text-white/20">-</p>
								</div>
								<div>
									<p
										v-if="record.totalHours"
										class="text-sm font-mono text-white"
										:class="
											record.totalHours >= workingHoursTarget
												? '!text-emerald-400 font-black scale-105 origin-left'
												: ''
										"
									>
										{{ record.totalHours.toFixed(2) }}
									</p>
									<p v-else class="text-sm text-white/20">-</p>
								</div>
								<div>
									<span
										v-if="record.status === 'complete'"
										class="text-[10px] px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-bold uppercase"
										>Complete</span
									>
									<span
										v-else-if="record.status === 'present'"
										class="text-[10px] px-2 py-1 rounded-full bg-emerald-500/15 text-emerald-400 font-bold uppercase"
										>Present</span
									>
									<span
										v-else-if="record.status === 'late'"
										class="text-[10px] px-2 py-1 rounded-full bg-amber-500/15 text-amber-400 font-bold uppercase"
										>Late</span
									>
									<span
										v-else-if="record.status === 'absent'"
										class="text-[10px] px-2 py-1 rounded-full bg-red-500/15 text-red-400 font-bold uppercase"
										>Absent</span
									>
									<span
										v-else-if="record.status === 'weekend'"
										class="text-[10px] px-2 py-1 rounded-full bg-white/5 text-white/30 font-bold uppercase"
										>Off</span
									>
									<span v-else class="text-[10px] text-white/20">-</span>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Mini Calendar -->
			<div class="hidden lg:block w-72 shrink-0">
				<StandardCalendar v-model="currentDate" :events="attendanceEvents" />
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useEmployeeStore } from "@/stores/employee";
import { useAttendanceStore } from "@/stores/attendance";
import StandardCalendar from "@/components/StandardCalendar.vue";

const employeeStore = useEmployeeStore();
const attendanceStore = useAttendanceStore();

const currentDate = ref(new Date());
const historyDays = ref(30);

// Computed from store
const isCheckedIn = computed(() => attendanceStore.isCheckedIn);
const isOnBreak = computed(() => attendanceStore.isOnBreak);
const totalHoursToday = computed(() => attendanceStore.totalHoursToday);
const overtimeHours = computed(() => attendanceStore.overtimeHours);
const workingHoursTarget = computed(() => attendanceStore.workingHoursTarget);
const roster = computed(() => attendanceStore.roster);
const canManageBreak = computed(() => attendanceStore.canManageBreak);
const formattedTimer = computed(() => attendanceStore.formattedWorkedTime);
const timerLabel = computed(() => attendanceStore.timerLabel);
const hasWorkedToday = computed(() => attendanceStore.workedSecondsToday > 0);

// Timer styling based on shift completion
const shiftComplete = computed(() => {
	return attendanceStore.shiftComplete;
});

const timerCircleClass = computed(() => {
	if (!hasWorkedToday.value && !isCheckedIn.value && !isOnBreak.value) return "bg-white/5";
	if (isOnBreak.value && !shiftComplete.value) return "bg-sky-500/10";
	return shiftComplete.value ? "bg-emerald-500/10" : "bg-amber-500/10";
});

const timerTextClass = computed(() => {
	if (!hasWorkedToday.value && !isCheckedIn.value && !isOnBreak.value) return "text-white/40";
	if (isOnBreak.value && !shiftComplete.value) return "text-sky-400";
	return shiftComplete.value ? "text-emerald-400" : "text-amber-400";
});

// Attendance events for calendar dots
const attendanceEvents = computed(() => {
	return (attendanceStore.history || [])
		.filter((log) => log.log_type === "IN")
		.map((log) => log.time.split("T")[0]);
});

// Daily records from history
const dailyRecords = computed(() => {
	const records = [];
	const history = attendanceStore.history || [];

	// Group logs by date
	const logsByDate = {};
	history.forEach((log) => {
		if (!log.time) return;
		const dateStr = log.time.split("T")[0];
		if (!logsByDate[dateStr]) {
			logsByDate[dateStr] = { logs: [], date: dateStr };
		}
		logsByDate[dateStr].logs.push(log);
	});

	// Convert to array and process
	Object.values(logsByDate).forEach((dayData) => {
		const date = new Date(dayData.date);
		const dayOfWeek = date.getDay();
		const isWeekend = dayOfWeek === 0 || dayOfWeek === 6;

		// Find first IN and last OUT
		const inLogs = dayData.logs.filter((l) => l.log_type === "IN");
		const outLogs = dayData.logs.filter((l) => l.log_type === "OUT");

		const clockIn = inLogs.length > 0 ? inLogs[0].time : null;
		const clockOut = outLogs.length > 0 ? outLogs[outLogs.length - 1].time : null;

		// Calculate total hours from all IN/OUT pairs so breaks do not count as worked time.
		let totalHours = 0;
		let activeClockIn = null;
		const sortedLogs = [...dayData.logs].sort((a, b) => new Date(a.time) - new Date(b.time));
		for (const log of sortedLogs) {
			if (log.log_type === "IN") {
				activeClockIn = new Date(log.time);
			} else if (log.log_type === "OUT" && activeClockIn) {
				totalHours += Math.max(0, new Date(log.time) - activeClockIn) / (1000 * 60 * 60);
				activeClockIn = null;
			}
		}

		// Determine status
		let status = "";
		const targetHours = workingHoursTarget.value;

		if (isWeekend) {
			status = "weekend";
		} else if (clockIn) {
			// Check if late (after shift start time or 9 AM)
			const inTime = new Date(clockIn);
			const lateThreshold = new Date(date);
			const startTime = roster.value?.start_time
				? roster.value.start_time.split(":")
				: [9, 0];
			lateThreshold.setHours(parseInt(startTime[0]), parseInt(startTime[1]), 0);

			if (totalHours >= targetHours) {
				status = "complete";
			} else if (inTime > lateThreshold) {
				status = "late";
			} else {
				status = "present";
			}
		} else {
			const todayDate = new Date();
			todayDate.setHours(0, 0, 0, 0);
			const compareDate = new Date(date);
			compareDate.setHours(0, 0, 0, 0);
			if (compareDate < todayDate) {
				status = "absent";
			}
		}

		records.push({
			date: dayData.date,
			clockIn,
			clockOut,
			totalHours,
			status,
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
	const present = dailyRecords.value.filter((r) =>
		["present", "late", "complete"].includes(r.status)
	);
	const onTime = present.filter((r) => r.status !== "late");
	return present.length > 0 ? Math.round((onTime.length / present.length) * 100) : 100;
});

const averageShiftHours = computed(() => {
	const withHours = dailyRecords.value.filter((r) => r.totalHours > 0);
	if (withHours.length === 0) return 0;
	const total = withHours.reduce((sum, r) => sum + r.totalHours, 0);
	return (total / withHours.length).toFixed(1);
});

// Methods
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

async function loadMoreHistory() {
	historyDays.value += 30;
	const employeeId = employeeStore.employee?.name;
	if (employeeId) {
		await attendanceStore.fetchHistory(employeeId, historyDays.value);
	}
}

async function handleBreak() {
	try {
		if (isOnBreak.value) {
			await attendanceStore.endBreak();
		} else {
			await attendanceStore.startBreak();
		}
		const employeeId = employeeStore.employee?.name;
		if (employeeId) {
			attendanceStore.fetchHistory(employeeId, historyDays.value);
		}
	} catch (error) {
		console.error("Break action failed:", error);
	}
}

async function handleClockIn() {
	const employeeId = employeeStore.employee?.name;
	if (!employeeId) return;

	try {
		await attendanceStore.clockIn(employeeId, null, null);
		attendanceStore.fetchHistory(employeeId, historyDays.value);
	} catch (error) {
		console.error("Clock in failed:", error);
	}
}

async function handleClockOut() {
	const employeeId = employeeStore.employee?.name;
	if (!employeeId) return;

	try {
		await attendanceStore.clockOut(employeeId, null, null);
		attendanceStore.fetchHistory(employeeId, historyDays.value);
	} catch (error) {
		console.error("Clock out failed:", error);
	}
}

// Initialize
onMounted(async () => {
	await employeeStore.init();
	const employeeId = employeeStore.employee?.name;
	if (employeeId) {
		await attendanceStore.init(employeeId);
		await attendanceStore.fetchHistory(employeeId, historyDays.value);
	}
});
</script>
