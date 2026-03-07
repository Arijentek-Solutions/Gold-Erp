<template>
	<div class="flex flex-col gap-4 h-full overflow-hidden">
		<!-- Header -->
		<div class="flex items-center justify-between shrink-0">
			<div>
				<h1 class="text-xl sm:text-2xl font-bold text-white">My Roster</h1>
				<p class="text-xs sm:text-sm text-white/40">Your weekly work schedule</p>
			</div>
			<div class="flex items-center gap-2">
				<button
					@click="previousWeek"
					class="p-2 rounded-lg hover:bg-white/5 text-white/40 hover:text-white transition-colors"
				>
					<span class="material-symbols-outlined">chevron_left</span>
				</button>
				<button
					@click="goToToday"
					class="px-3 py-1.5 text-xs font-bold text-primary hover:text-yellow-400 transition-colors"
				>
					Today
				</button>
				<button
					@click="nextWeek"
					class="p-2 rounded-lg hover:bg-white/5 text-white/40 hover:text-white transition-colors"
				>
					<span class="material-symbols-outlined">chevron_right</span>
				</button>
			</div>
		</div>

		<!-- Week Range Display -->
		<div class="glass-card rounded-xl p-4 border border-white/5 shrink-0">
			<div class="flex items-center justify-between">
				<div>
					<p class="text-sm font-bold text-white">{{ weekRangeDisplay }}</p>
					<p class="text-[10px] text-white/40 mt-0.5">
						{{ roster?.employment_type || 'Full-time' }} Employee - {{ roster?.working_hours || 8 }} hrs/day
					</p>
				</div>
				<div class="text-right">
					<p class="text-[10px] text-white/30 uppercase tracking-widest">Weekly Target</p>
					<p class="text-lg font-bold font-mono text-white">{{ weeklyTargetHours }} hrs</p>
				</div>
			</div>
		</div>

		<!-- Weekly Grid -->
		<div class="flex-1 overflow-hidden">
			<div v-if="loading" class="h-full flex items-center justify-center">
				<div class="text-center">
					<div class="animate-spin rounded-full h-8 w-8 border-2 border-primary border-t-transparent mx-auto mb-3"></div>
					<p class="text-white/40 text-sm">Loading schedule...</p>
				</div>
			</div>

			<div v-else class="h-full overflow-y-auto custom-scrollbar">
				<!-- Day Headers -->
				<div class="grid grid-cols-7 gap-1 sm:gap-2 mb-2 sticky top-0 bg-[#1a1c23] py-2 z-10">
					<div v-for="day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']" :key="day"
						class="text-center text-[9px] sm:text-[10px] text-white/40 uppercase font-bold tracking-widest"
					>
						{{ day }}
					</div>
				</div>

				<!-- Week Days Grid -->
				<div class="grid grid-cols-7 gap-1 sm:gap-2">
					<div
						v-for="day in weeklySchedule"
						:key="day.date"
						class="glass-card rounded-xl p-2 sm:p-3 border transition-all"
						:class="[
							day.isToday
								? 'border-primary/50 bg-primary/5'
								: day.status === 'off'
								? 'border-white/5 bg-white/[0.02]'
								: 'border-white/10 hover:border-white/20',
						]"
					>
						<!-- Date Header -->
						<div class="flex items-center justify-between mb-2">
							<div>
								<p class="text-xs sm:text-sm font-bold" :class="day.isToday ? 'text-primary' : 'text-white'">
									{{ day.day_num }}
								</p>
								<p class="text-[8px] sm:text-[10px] text-white/30">{{ day.day_short }}</p>
							</div>
							<span
								v-if="day.isToday"
								class="text-[8px] px-1.5 py-0.5 rounded-full bg-primary/20 text-primary font-bold uppercase"
							>
								Today
							</span>
						</div>

						<!-- Shift Info -->
						<div v-if="day.shift && day.status !== 'off'" class="space-y-1.5">
							<div class="flex items-center gap-1">
								<span class="material-symbols-outlined text-[12px] text-white/30">schedule</span>
								<p class="text-[10px] sm:text-xs text-white/60">
									{{ day.shift.start_time ? formatTime(day.shift.start_time) : '09:00' }}
									-
									{{ day.shift.end_time ? formatTime(day.shift.end_time) : '17:00' }}
								</p>
							</div>

							<!-- Hours Progress -->
							<div class="h-1.5 bg-white/5 rounded-full overflow-hidden">
								<div
									class="h-full rounded-full transition-all"
									:class="day.total_hours >= day.shift.working_hours ? 'bg-emerald-500' : 'bg-amber-500'"
									:style="{ width: `${Math.min((day.total_hours / day.shift.working_hours) * 100, 100)}%` }"
								></div>
							</div>

							<div class="flex items-center justify-between text-[9px] sm:text-[10px]">
								<span class="text-white/40">{{ day.total_hours.toFixed(1) }} hrs</span>
								<span class="font-bold" :class="day.total_hours >= day.shift.working_hours ? 'text-emerald-400' : 'text-white/60'">
									{{ day.shift.working_hours }}h target
								</span>
							</div>

							<!-- Check-ins -->
							<div v-if="day.checkins.length > 0" class="pt-1.5 border-t border-white/5 mt-1.5">
								<div v-for="(checkin, idx) in day.checkins.slice(0, 2)" :key="idx" class="flex items-center gap-1 text-[9px]">
									<span :class="checkin.log_type === 'IN' ? 'text-emerald-400' : 'text-blue-400'">
										{{ checkin.log_type === 'IN' ? '→' : '←' }}
									</span>
									<span class="text-white/50">{{ formatTime(checkin.time) }}</span>
								</div>
								<p v-if="day.checkins.length > 2" class="text-[8px] text-white/30 mt-0.5">
									+{{ day.checkins.length - 2 }} more
								</p>
							</div>
						</div>

						<!-- Day Off -->
						<div v-else-if="day.status === 'off'" class="text-center py-4">
							<span class="material-symbols-outlined text-xl text-white/10">weekend</span>
							<p class="text-[9px] text-white/20 mt-1">Day Off</p>
						</div>

						<!-- Past Day with no data -->
						<div v-else-if="day.is_past" class="text-center py-4">
							<span class="material-symbols-outlined text-xl text-red-400/30">event_busy</span>
							<p class="text-[9px] text-red-400/40 mt-1">Absent</p>
						</div>

						<!-- Future day -->
						<div v-else class="text-center py-4">
							<span class="material-symbols-outlined text-xl text-white/10">event</span>
							<p class="text-[9px] text-white/20 mt-1">Scheduled</p>
						</div>
					</div>
				</div>

				<!-- Weekly Summary -->
				<div class="mt-4 glass-card rounded-xl p-4 border border-white/5">
					<h3 class="text-sm font-bold text-white mb-3">Weekly Summary</h3>
					<div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
						<div>
							<p class="text-[9px] text-white/30 uppercase tracking-widest mb-1">Working Days</p>
							<p class="text-lg font-bold font-mono text-white">{{ summary?.total_working_days || 0 }}</p>
						</div>
						<div>
							<p class="text-[9px] text-white/30 uppercase tracking-widest mb-1">Completed</p>
							<p class="text-lg font-bold font-mono text-emerald-400">{{ summary?.completed_days || 0 }}</p>
						</div>
						<div>
							<p class="text-[9px] text-white/30 uppercase tracking-widest mb-1">Hours Worked</p>
							<p class="text-lg font-bold font-mono text-white">{{ summary?.total_hours?.toFixed(1) || 0 }}</p>
						</div>
						<div>
							<p class="text-[9px] text-white/30 uppercase tracking-widest mb-1">Target Hours</p>
							<p class="text-lg font-bold font-mono text-primary">{{ summary?.target_hours || 0 }}</p>
						</div>
					</div>

					<!-- Progress Bar -->
					<div class="mt-4">
						<div class="flex items-center justify-between text-[10px] mb-1">
							<span class="text-white/40">Progress</span>
							<span class="text-white font-bold">{{ weeklyProgressPercent }}%</span>
						</div>
						<div class="h-2 bg-white/5 rounded-full overflow-hidden">
							<div
								class="h-full rounded-full transition-all"
								:class="weeklyProgressPercent >= 100 ? 'bg-emerald-500' : 'bg-primary'"
								:style="{ width: `${Math.min(weeklyProgressPercent, 100)}%` }"
							></div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { createResource } from "frappe-ui";
import { useEmployeeStore } from "@/stores/employee";

const employeeStore = useEmployeeStore();

const weekStart = ref(getWeekStart(new Date()));
const roster = ref(null);
const weeklySchedule = ref([]);
const summary = ref(null);
const loading = ref(false);

// Resource for weekly roster
const weeklyRosterResource = createResource({
	url: "zevar_core.api.attendance.get_weekly_roster",
	auto: false,
	onSuccess(data) {
		roster.value = data.roster;
		weeklySchedule.value = data.schedule || [];
		summary.value = data.summary || {};
		loading.value = false;
	},
	onError() {
		loading.value = false;
	},
});

// Computed
const weekRangeDisplay = computed(() => {
	const start = weekStart.value;
	const end = new Date(start);
	end.setDate(end.getDate() + 6);

	const startStr = start.toLocaleDateString("en-US", { month: "short", day: "numeric" });
	const endStr = end.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });

	return `${startStr} - ${endStr}`;
});

const weeklyTargetHours = computed(() => {
	return summary.value?.target_hours || (roster.value?.working_hours || 8) * 5;
});

const weeklyProgressPercent = computed(() => {
	if (!summary.value?.target_hours) return 0;
	return Math.round((summary.value.total_hours / summary.value.target_hours) * 100);
});

// Methods
function getWeekStart(date) {
	const d = new Date(date);
	const day = d.getDay();
	const diff = d.getDate() - day + (day === 0 ? -6 : 1);
	return new Date(d.setDate(diff));
}

function formatTime(timeStr) {
	if (!timeStr) return "";
	// Handle both "HH:MM:SS" and ISO format
	let hours, minutes;
	if (timeStr.includes("T")) {
		const date = new Date(timeStr);
		hours = date.getHours();
		minutes = date.getMinutes();
	} else {
		const parts = timeStr.split(":");
		hours = parseInt(parts[0]);
		minutes = parseInt(parts[1]);
	}

	const period = hours >= 12 ? "PM" : "AM";
	hours = hours % 12 || 12;
	return `${hours}:${minutes.toString().padStart(2, "0")} ${period}`;
}

async function fetchWeeklyRoster() {
	const employeeId = employeeStore.employee?.name;
	if (!employeeId) return;

	loading.value = true;
	await weeklyRosterResource.fetch({
		employee_id: employeeId,
		start_date: weekStart.value.toISOString().split("T")[0],
	});
}

function previousWeek() {
	const newStart = new Date(weekStart.value);
	newStart.setDate(newStart.getDate() - 7);
	weekStart.value = newStart;
	fetchWeeklyRoster();
}

function nextWeek() {
	const newStart = new Date(weekStart.value);
	newStart.setDate(newStart.getDate() + 7);
	weekStart.value = newStart;
	fetchWeeklyRoster();
}

function goToToday() {
	weekStart.value = getWeekStart(new Date());
	fetchWeeklyRoster();
}

// Watch for employee changes
watch(() => employeeStore.employee, (emp) => {
	if (emp?.name) {
		fetchWeeklyRoster();
	}
}, { immediate: false });

// Initialize
onMounted(async () => {
	await employeeStore.init();
	if (employeeStore.employee?.name) {
		fetchWeeklyRoster();
	}
});
</script>
