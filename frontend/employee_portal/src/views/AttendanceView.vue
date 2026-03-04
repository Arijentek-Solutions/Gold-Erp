<template>
	<div class="flex flex-col gap-8">
		<!-- Stats Row -->
		<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
			<div class="glass-card p-6 rounded-2xl relative overflow-hidden group">
				<div
					class="absolute inset-0 bg-primary/5 group-hover:bg-primary/10 transition-colors"
				></div>
				<h3 class="text-xs font-bold text-white/40 uppercase mb-2 relative z-10">
					Total Hours This Month
				</h3>
				<div class="flex items-end gap-3 relative z-10">
					<span class="text-4xl font-bold font-mono text-white">{{
						totalHours.toFixed(1)
					}}</span>
					<span class="text-emerald-glow text-xs font-bold mb-1">hours</span>
				</div>
				<div class="absolute right-4 top-1/2 -translate-y-1/2">
					<div class="relative w-16 h-16 flex items-center justify-center">
						<svg class="w-full h-full transform -rotate-90">
							<circle
								class="text-white/5"
								cx="32"
								cy="32"
								fill="transparent"
								r="28"
								stroke="currentColor"
								stroke-width="4"
							></circle>
							<circle
								class="text-emerald-glow"
								cx="32"
								cy="32"
								fill="transparent"
								r="28"
								stroke="currentColor"
								:stroke-dasharray="175"
								:stroke-dashoffset="175 - (175 * hoursProgress) / 100"
								stroke-width="4"
							></circle>
						</svg>
						<span class="absolute text-[10px] font-bold">{{ hoursProgress }}%</span>
					</div>
				</div>
			</div>

			<div class="glass-card p-6 rounded-2xl relative overflow-hidden group">
				<div
					class="absolute inset-0 bg-gold-accent/5 group-hover:bg-gold-accent/10 transition-colors"
				></div>
				<h3 class="text-xs font-bold text-white/40 uppercase mb-2 relative z-10">
					On-time Rate
				</h3>
				<div class="flex items-end gap-3 relative z-10">
					<span class="text-4xl font-bold font-mono text-white">{{ onTimeRate }}%</span>
					<span class="text-gold-accent text-xs font-bold mb-1">
						{{
							onTimeRate >= 90
								? "Excellent"
								: onTimeRate >= 75
								? "Good"
								: "Needs Work"
						}}
					</span>
				</div>
				<div class="absolute right-4 top-1/2 -translate-y-1/2">
					<div class="relative w-16 h-16 flex items-center justify-center">
						<svg class="w-full h-full transform -rotate-90">
							<circle
								class="text-white/5"
								cx="32"
								cy="32"
								fill="transparent"
								r="28"
								stroke="currentColor"
								stroke-width="4"
							></circle>
							<circle
								class="text-gold-accent"
								cx="32"
								cy="32"
								fill="transparent"
								r="28"
								stroke="currentColor"
								:stroke-dasharray="175"
								:stroke-dashoffset="175 - (175 * onTimeRate) / 100"
								stroke-width="4"
							></circle>
						</svg>
						<span class="absolute text-[10px] font-bold">{{ onTimeRate }}%</span>
					</div>
				</div>
			</div>

			<div class="glass-card p-6 rounded-2xl relative overflow-hidden group">
				<div
					class="absolute inset-0 bg-blue-500/5 group-hover:bg-blue-500/10 transition-colors"
				></div>
				<h3 class="text-xs font-bold text-white/40 uppercase mb-2 relative z-10">
					Average Shift
				</h3>
				<div class="relative z-10">
					<span class="text-4xl font-bold font-mono text-white"
						>{{ averageShiftHours }}h</span
					>
					<span class="text-sm text-white/40">{{ averageShiftMinutes }}m</span>
					<div class="mt-3 h-1 w-full bg-white/10 rounded-full overflow-hidden">
						<div
							class="h-full bg-blue-500 rounded-full shadow-[0_0_10px_rgba(59,130,246,0.5)] transition-all"
							:style="{
								width: `${Math.min(
									100,
									(averageShiftHours / workingHoursTarget) * 100
								)}%`,
							}"
						></div>
					</div>
				</div>
			</div>
		</div>

		<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
			<!-- Calendar Section -->
			<div class="lg:col-span-2 glass-card rounded-2xl p-8 border border-white/5">
				<div class="flex items-center justify-between mb-8">
					<div>
						<h2 class="text-2xl font-bold text-white">{{ currentMonthYear }}</h2>
						<p class="text-sm text-white/40">Monthly Attendance Performance</p>
					</div>
					<div class="flex gap-2">
						<button
							@click="previousMonth"
							class="p-2 rounded-lg hover:bg-white/5 text-white/60 hover:text-white transition-colors"
						>
							<span class="material-symbols-outlined">chevron_left</span>
						</button>
						<button
							@click="nextMonth"
							class="p-2 rounded-lg hover:bg-white/5 text-white/60 hover:text-white transition-colors"
						>
							<span class="material-symbols-outlined">chevron_right</span>
						</button>
					</div>
				</div>

				<!-- Calendar Grid -->
				<div class="grid grid-cols-7 gap-y-8 gap-x-4 text-center">
					<div class="text-[10px] font-bold uppercase text-white/30 mb-2">Mon</div>
					<div class="text-[10px] font-bold uppercase text-white/30 mb-2">Tue</div>
					<div class="text-[10px] font-bold uppercase text-white/30 mb-2">Wed</div>
					<div class="text-[10px] font-bold uppercase text-white/30 mb-2">Thu</div>
					<div class="text-[10px] font-bold uppercase text-white/30 mb-2">Fri</div>
					<div class="text-[10px] font-bold uppercase text-white/30 mb-2">Sat</div>
					<div class="text-[10px] font-bold uppercase text-white/30 mb-2">Sun</div>

					<!-- Empty cells for days before month start -->
					<div
						v-for="i in firstDayOfMonth"
						:key="'empty-' + i"
						class="aspect-square"
					></div>

					<!-- Days -->
					<button
						v-for="day in calendarDays"
						:key="day.date"
						class="aspect-square rounded-full flex flex-col items-center justify-center relative transition-all group"
						:class="[
							day.status === 'present' ? 'hover:bg-white/5' : '',
							day.status === 'absent' ? 'hover:bg-red-500/10' : '',
							day.isToday
								? 'border border-primary text-primary shadow-[0_0_10px_rgba(244,192,37,0.2)]'
								: 'text-white/60',
						]"
					>
						<span class="text-sm font-medium">{{ day.day }}</span>
						<span
							v-if="day.status === 'present'"
							class="w-1 h-1 rounded-full bg-emerald-glow mt-1"
						></span>
						<span
							v-if="day.status === 'absent'"
							class="w-1 h-1 rounded-full bg-red-400 mt-1"
						></span>
						<span
							v-if="day.status === 'leave'"
							class="w-1 h-1 rounded-full bg-blue-400 mt-1"
						></span>
						<span
							v-if="day.status === 'holiday'"
							class="w-1 h-1 rounded-full bg-purple-400 mt-1"
						></span>
					</button>
				</div>

				<!-- Legend -->
				<div class="mt-6 flex gap-6 justify-center text-xs text-white/40">
					<div class="flex items-center gap-2">
						<span class="w-2 h-2 rounded-full bg-emerald-glow"></span>
						<span>Present</span>
					</div>
					<div class="flex items-center gap-2">
						<span class="w-2 h-2 rounded-full bg-red-400"></span>
						<span>Absent</span>
					</div>
					<div class="flex items-center gap-2">
						<span class="w-2 h-2 rounded-full bg-blue-400"></span>
						<span>Leave</span>
					</div>
					<div class="flex items-center gap-2">
						<span class="w-2 h-2 rounded-full bg-purple-400"></span>
						<span>Holiday</span>
					</div>
				</div>
			</div>

			<!-- Recent Activity / Timeline -->
			<div class="col-span-1 space-y-6">
				<div class="flex items-center justify-between">
					<h3 class="font-bold text-lg text-white">Recent Activity</h3>
				</div>

				<div class="space-y-4">
					<!-- No activity message -->
					<div v-if="recentActivity.length === 0" class="text-center py-8">
						<div
							class="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-4"
						>
							<span class="material-symbols-outlined text-3xl text-white/20"
								>history</span
							>
						</div>
						<p class="text-white/40 text-sm">No recent activity</p>
						<p class="text-white/20 text-xs mt-1">Clock in to start tracking</p>
					</div>

					<!-- Activity items -->
					<div
						v-for="log in recentActivity"
						:key="log.name"
						class="glass-card p-4 rounded-xl border border-white/5 flex gap-4 items-center group hover:bg-white/5 transition-colors"
					>
						<div
							class="w-10 h-10 rounded-full flex items-center justify-center"
							:class="getLogStyle(log.log_type).bg"
						>
							<span
								class="material-symbols-outlined text-lg"
								:class="getLogStyle(log.log_type).text"
							>
								{{ getLogStyle(log.log_type).icon }}
							</span>
						</div>
						<div class="flex-1">
							<div class="flex justify-between items-center mb-1">
								<p class="text-sm font-bold text-white">
									{{ getLogStyle(log.log_type).label }}
								</p>
								<span
									v-if="log.log_type === 'IN'"
									class="text-[10px] bg-emerald-glow/20 text-emerald-glow px-1.5 py-0.5 rounded font-bold uppercase"
								>
									{{ log.on_time !== false ? "On Time" : "Late" }}
								</span>
							</div>
							<p class="text-xs text-white/40">{{ formatDateTime(log.time) }}</p>
						</div>
					</div>
				</div>

				<button
					@click="loadMoreHistory"
					class="w-full py-4 text-xs font-bold uppercase tracking-widest text-white/40 hover:text-white glass-card rounded-xl hover:bg-white/5 transition-colors"
				>
					Load Previous History
				</button>
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
	return currentDate.value.toLocaleDateString("en-US", { month: "long", year: "numeric" });
});

// Get first day of month (0 = Sunday, 1 = Monday, etc.)
const firstDayOfMonth = computed(() => {
	const firstDay = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth(), 1);
	// Adjust for Monday start (0 = Monday, 6 = Sunday)
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

		// Check status from attendance history
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

// Stats
const totalHours = computed(() => {
	return attendanceStore.totalHoursToday || 0;
});

const hoursProgress = computed(() => {
	const target = (attendanceStore.workingHoursTarget || 8) * 22; // ~22 working days
	const actual = totalHours.value;
	return Math.min(100, Math.round((actual / target) * 100));
});

const onTimeRate = computed(() => {
	// Placeholder - would calculate from actual check-in times
	return 95;
});

const averageShiftHours = computed(() => {
	const hours = attendanceStore.workingHoursTarget || 8;
	return Math.floor(hours);
});

const averageShiftMinutes = computed(() => {
	const hours = attendanceStore.workingHoursTarget || 8;
	return Math.round((hours % 1) * 60);
});

const workingHoursTarget = computed(() => {
	return attendanceStore.roster?.working_hours || 8;
});

// Recent activity
const recentActivity = computed(() => {
	return attendanceStore.history.slice(0, 5);
});

// Methods
function getDayStatus(date) {
	// Check if it's a weekend
	const dayOfWeek = date.getDay();
	if (dayOfWeek === 0 || dayOfWeek === 6) {
		return "weekend";
	}

	// Check from history
	const dateStr = date.toISOString().split("T")[0];
	const logs = attendanceStore.history.filter((log) => log.time && log.time.startsWith(dateStr));

	if (logs.length > 0) {
		return "present";
	}

	// Future date
	const today = new Date();
	if (date > today) {
		return "";
	}

	return "absent";
}

function getLogStyle(logType) {
	switch (logType) {
		case "IN":
			return {
				bg: "bg-emerald-glow/10 border border-emerald-glow/20",
				text: "text-emerald-glow",
				icon: "login",
				label: "Shift Started",
			};
		case "OUT":
			return {
				bg: "bg-blue-500/10 border border-blue-500/20",
				text: "text-blue-400",
				icon: "logout",
				label: "Shift Ended",
			};
		default:
			return {
				bg: "bg-white/5 border border-white/10",
				text: "text-white/40",
				icon: "circle",
				label: "Activity",
			};
	}
}

function formatDateTime(timeStr) {
	if (!timeStr) return "";
	const date = new Date(timeStr);
	return date.toLocaleDateString("en-US", {
		month: "short",
		day: "numeric",
		hour: "numeric",
		minute: "2-digit",
	});
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
	const employeeId = employeeStore.employee?.employee_id;
	if (employeeId) {
		await attendanceStore.fetchHistory(employeeId, historyDays.value);
	}
}

// Initialize
onMounted(async () => {
	await employeeStore.init();
	const employeeId = employeeStore.employee?.employee_id;
	if (employeeId) {
		attendanceStore.init(employeeId);
		await attendanceStore.fetchHistory(employeeId, historyDays.value);
	}
});
</script>
