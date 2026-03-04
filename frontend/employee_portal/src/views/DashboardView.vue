<template>
	<div class="grid grid-cols-12 gap-6 max-w-7xl mx-auto h-[calc(100vh-6rem)]">
		<!-- Left Column: Clock & Widgets -->
		<div class="col-span-12 lg:col-span-8 flex flex-col gap-6 h-full">
			<!-- Clock Section -->
			<div
				class="flex-1 flex flex-col items-center justify-center py-2 glass-card rounded-[2rem] border border-white/5 relative bg-gradient-to-b from-white/5 to-transparent overflow-visible"
			>
				<!-- Background decorative elements -->
				<div
					class="absolute top-0 left-0 w-full h-full diamond-pattern opacity-30 pointer-events-none rounded-[2rem] overflow-hidden"
				></div>
				<div
					class="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/40 pointer-events-none rounded-[2rem]"
				></div>

				<div class="relative group z-10 scale-100">
					<!-- Outer Bezel (Massive) -->
					<div
						class="w-[380px] h-[380px] rounded-full metallic-bezel border-[4px] border-[#2a2a2a] flex items-center justify-center relative p-1 shadow-[0_0_60px_rgba(0,0,0,0.8)]"
					>
						<!-- Glowing Border Ring -->
						<div
							class="absolute inset-0 rounded-full border border-primary/20 shadow-[0_0_40px_rgba(252,211,77,0.1)]"
						></div>

						<!-- Inner Bezel Detail -->
						<div
							class="w-full h-full rounded-full border-[10px] border-[#0a0c1a] shadow-inner flex items-center justify-center relative bg-[#05070a]"
						>
							<!-- Digital Face -->
							<div
								class="w-full h-full rounded-full flex flex-col items-center justify-center relative overflow-hidden bg-[radial-gradient(circle_at_center,_#1a1d2d_0%,_#05070a_70%)]"
							>
								<!-- Subtle grid/texture on face -->
								<div
									class="absolute inset-0 opacity-10"
									style="
										background-image: radial-gradient(
											#fff 1px,
											transparent 1px
										);
										background-size: 20px 20px;
									"
								></div>

								<div
									class="absolute top-[22%] text-[10px] text-white/30 tracking-[0.4em] font-bold uppercase font-display"
								>
									{{ shiftLabel }}
								</div>

								<!-- Huge Timer -->
								<div
									class="text-[4.5rem] leading-none font-mono font-bold tracking-tighter mt-2 transition-colors duration-500 z-10 drop-shadow-2xl tabular-nums"
									:class="getTimerColor"
								>
									{{ displayTime }}
								</div>

								<!-- Active Indicators -->
								<div
									class="absolute bottom-[22%] flex gap-3"
									v-if="attendance.isCheckedIn"
								>
									<span
										class="w-2 h-2 rounded-full animate-pulse shadow-[0_0_10px_currentColor]"
										:class="getDotColor"
									></span>
									<span
										class="w-2 h-2 rounded-full opacity-30"
										:class="getDotColor"
									></span>
									<span
										class="w-2 h-2 rounded-full opacity-20"
										:class="getDotColor"
									></span>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Buttons -->
				<div class="mt-8 flex gap-4 w-full max-w-sm z-10">
					<button
						@click="handleClockIn"
						:disabled="attendance.isCheckedIn || attendance.loading"
						class="flex-1 h-14 rounded-xl flex items-center justify-center gap-2 transition-all relative font-bold tracking-widest text-sm uppercase"
						:class="[
							!attendance.isCheckedIn
								? 'bg-[#FCD34D] text-black hover:bg-[#FDE047] hover:scale-[1.02] shadow-[0_0_30px_rgba(252,211,77,0.3)]'
								: 'bg-white/5 border border-white/5 text-white/20 cursor-not-allowed',
						]"
					>
						<span v-if="attendance.loading" class="animate-spin">⏳</span>
						<span v-else>Clock In</span>
					</button>

					<button
						@click="handleClockOut"
						:disabled="!attendance.isCheckedIn || attendance.loading"
						class="flex-1 h-14 rounded-xl flex items-center justify-center gap-2 transition-all relative font-bold tracking-widest text-sm uppercase"
						:class="[
							attendance.isCheckedIn
								? 'bg-[#1a1a1a] border border-white/10 text-white hover:bg-[#252525] hover:border-white/20 hover:text-red-400 shadow-lg'
								: 'bg-white/5 border border-white/5 text-white/20 cursor-not-allowed',
						]"
					>
						<span v-if="attendance.loading" class="animate-spin">⏳</span>
						<span v-else>Clock Out</span>
					</button>
				</div>
			</div>

			<!-- Bottom Info Row -->
			<div class="grid grid-cols-3 gap-6 shrink-0 h-72">
				<!-- Profile & Designation -->
				<div
					class="glass-card rounded-2xl p-5 border border-white/5 flex flex-col justify-between relative overflow-hidden group hover:border-white/10 transition-colors"
				>
					<div
						class="absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity"
					>
						<span class="material-symbols-outlined text-6xl">badge</span>
					</div>
					<div>
						<p
							class="text-[10px] text-white/40 font-bold uppercase tracking-wider mb-1"
						>
							My Profile
						</p>
						<div class="flex items-center gap-3 mt-1">
							<div
								class="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-orange-500 flex items-center justify-center text-black font-bold text-sm shadow-lg shadow-primary/20"
							>
								{{ userInitials }}
							</div>
							<div>
								<p class="text-sm font-bold text-white leading-tight">
									{{ employeeName }}
								</p>
								<p class="text-[10px] text-primary mt-0.5">
									{{ employeeDesignation }}
								</p>
							</div>
						</div>
					</div>
					<button
						class="mt-2 py-2 px-3 bg-white/5 hover:bg-white/10 rounded-lg text-[10px] font-bold text-white border border-white/5 flex items-center gap-2 w-full justify-center transition-all group-hover:bg-white/10"
					>
						<span class="material-symbols-outlined text-[14px]">account_box</span>
						View Profile
					</button>
				</div>

				<!-- Reporting Manager -->
				<div
					class="glass-card rounded-2xl p-5 border border-white/5 flex flex-col justify-between relative overflow-hidden group hover:border-white/10 transition-colors"
				>
					<div
						class="absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity"
					>
						<span class="material-symbols-outlined text-6xl">supervisor_account</span>
					</div>
					<div>
						<p
							class="text-[10px] text-white/40 font-bold uppercase tracking-wider mb-1"
						>
							Reporting To
						</p>
						<div class="flex items-center gap-3 mt-2">
							<div
								class="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400 font-bold text-xs ring-1 ring-blue-500/30"
							>
								{{ managerInitials }}
							</div>
							<div>
								<p class="text-sm font-bold text-white">{{ managerName }}</p>
								<p class="text-[10px] text-white/50">{{ managerDesignation }}</p>
							</div>
						</div>
					</div>
					<router-link to="/team" class="block">
						<button
							class="mt-auto py-2 px-3 bg-white/5 hover:bg-white/10 rounded-lg text-[10px] font-bold text-white/70 border border-white/5 w-full transition-all"
						>
							View Team
						</button>
					</router-link>
				</div>

				<!-- Payslip -->
				<div
					class="glass-card rounded-2xl p-5 border border-white/5 flex flex-col justify-between relative overflow-hidden group hover:border-white/10 transition-colors"
				>
					<div
						class="absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity"
					>
						<span class="material-symbols-outlined text-6xl">payments</span>
					</div>
					<div>
						<p
							class="text-[10px] text-white/40 font-bold uppercase tracking-wider mb-1"
						>
							Payroll
						</p>
						<p class="text-base font-bold text-white">{{ payslipMonth }}</p>
						<p
							v-if="payslipStatus"
							class="text-[10px] text-emerald-400 mt-1 flex items-center gap-1 bg-emerald-400/10 w-fit px-1.5 py-0.5 rounded"
						>
							<span class="material-symbols-outlined text-[10px]">check_circle</span>
							{{ payslipStatus }}
						</p>
						<p v-else class="text-[10px] text-white/40 mt-1">No payslip available</p>
					</div>
					<router-link to="/payroll" class="block">
						<button
							class="mt-4 py-2 px-3 bg-primary/10 hover:bg-primary/20 rounded-lg text-[10px] font-bold text-primary border border-primary/20 flex items-center justify-center gap-2 w-full transition-all"
						>
							<span class="material-symbols-outlined text-[14px]">visibility</span>
							View Slip
						</button>
					</router-link>
				</div>
			</div>
		</div>

		<!-- Right Column: Split Activity & Todos -->
		<div class="col-span-12 lg:col-span-4 flex flex-col gap-6 h-full">
			<!-- Top: Notifications / Activity -->
			<div class="glass-card rounded-[2rem] p-6 h-1/2 border border-white/10 flex flex-col">
				<div class="flex items-center justify-between mb-4">
					<h3 class="font-bold text-lg text-white font-display">Activity & Alerts</h3>
					<span
						class="w-2 h-2 bg-primary rounded-full animate-pulse shadow-[0_0_8px_#FCD34D]"
					></span>
				</div>

				<div class="flex-1 overflow-y-auto custom-scrollbar space-y-4 pr-2">
					<!-- No activity message -->
					<div v-if="recentActivity.length === 0" class="text-center text-white/40 py-8">
						<span class="material-symbols-outlined text-4xl mb-2">history</span>
						<p class="text-sm">No recent activity</p>
					</div>

					<!-- Activity items -->
					<div
						v-for="log in recentActivity"
						:key="log.id"
						class="flex gap-3 relative group opacity-60 hover:opacity-100 transition-opacity"
					>
						<div
							class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 border bg-[#0a0c1a]"
							:class="getActivityIconClass(log.type)"
						>
							<span class="material-symbols-outlined text-[16px]">{{
								log.icon
							}}</span>
						</div>
						<div>
							<p
								class="text-xs font-bold text-white transition-colors group-hover:text-primary leading-snug"
							>
								{{ log.title }}
							</p>
							<p class="text-[9px] text-white/30 mt-0.5">{{ log.time }}</p>
						</div>
					</div>
				</div>
			</div>

			<!-- Bottom: Todos -->
			<div class="glass-card rounded-[2rem] p-6 h-1/2 border border-white/10 flex flex-col">
				<div class="flex items-center justify-between mb-4">
					<h3 class="font-bold text-lg text-white font-display">My Tasks</h3>
					<button
						@click="showAddTodo = true"
						class="w-6 h-6 rounded-full bg-white/5 hover:bg-white/10 flex items-center justify-center text-white/50 hover:text-white transition-all border border-white/5"
					>
						<span class="material-symbols-outlined text-[16px]">add</span>
					</button>
				</div>

				<div class="flex-1 overflow-y-auto custom-scrollbar space-y-2 pr-2">
					<!-- Gameplan not installed -->
					<div v-if="!tasksStore.gameplanInstalled" class="text-center py-4">
						<p class="text-xs text-white/40">
							Gameplan not installed. Showing personal todos only.
						</p>
					</div>

					<!-- No tasks -->
					<div
						v-if="tasksStore.openTodos.length === 0"
						class="text-center text-white/40 py-8"
					>
						<span class="material-symbols-outlined text-4xl mb-2">check_circle</span>
						<p class="text-sm">No pending tasks</p>
					</div>

					<!-- Task items -->
					<div
						v-for="todo in tasksStore.openTodos.slice(0, 5)"
						:key="todo.id"
						@click="toggleTodo(todo.id, todo.status)"
						class="group flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-all border border-transparent hover:border-white/5 cursor-pointer"
					>
						<div
							class="w-4 h-4 rounded border border-white/20 flex items-center justify-center group-hover:border-primary transition-colors"
						>
							<span
								class="material-symbols-outlined text-[12px] text-transparent group-hover:text-white/20"
								>check</span
							>
						</div>
						<div class="flex-1 min-w-0">
							<p
								class="text-xs font-medium text-white group-hover:text-primary/90 transition-colors truncate"
							>
								{{ todo.description }}
							</p>
							<div class="flex items-center gap-2 mt-0.5">
								<span class="text-[9px] text-white/30">{{
									formatDate(todo.date)
								}}</span>
								<span
									v-if="todo.priority === 'High'"
									class="w-1.5 h-1.5 rounded-full bg-red-400"
								></span>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Add Todo Modal -->
		<Teleport to="body">
			<div
				v-if="showAddTodo"
				class="fixed inset-0 z-50 flex items-center justify-center p-4"
				@click.self="showAddTodo = false"
			>
				<div class="absolute inset-0 bg-black/60"></div>
				<div
					class="relative bg-[#111420] rounded-2xl p-6 w-full max-w-md border border-white/10"
				>
					<h3 class="font-bold text-white text-lg mb-4">Add Task</h3>
					<input
						v-model="newTodoText"
						type="text"
						placeholder="Task description..."
						class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-primary/50 mb-4"
						@keyup.enter="addTodo"
					/>
					<div class="flex gap-3">
						<button
							@click="showAddTodo = false"
							class="flex-1 py-3 bg-white/5 hover:bg-white/10 rounded-xl text-white/60 text-sm font-bold transition-colors"
						>
							Cancel
						</button>
						<button
							@click="addTodo"
							:disabled="!newTodoText.trim()"
							class="flex-1 py-3 bg-primary text-black rounded-xl text-sm font-bold hover:bg-yellow-400 transition-colors disabled:opacity-50"
						>
							Add Task
						</button>
					</div>
				</div>
			</div>
		</Teleport>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, inject } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useEmployeeStore } from "@/stores/employee";
import { useAttendanceStore } from "@/stores/attendance";
import { useTasksStore } from "@/stores/tasks";
import { usePayrollStore } from "@/stores/payroll";

const auth = useAuthStore();
const employeeStore = useEmployeeStore();
const attendance = useAttendanceStore();
const tasksStore = useTasksStore();
const payrollStore = usePayrollStore();

const showAddTodo = ref(false);
const newTodoText = ref("");
const displayTime = ref("00:00:00");
let timerInterval = null;

// Computed from employee store
const employeeName = computed(() => {
	return employeeStore.employee?.employee_name || auth.user?.full_name || "Employee";
});

const employeeDesignation = computed(() => {
	return employeeStore.employee?.designation || "Staff";
});

const userInitials = computed(() => {
	const name = employeeName.value;
	return name
		.split(" ")
		.map((n) => n[0])
		.join("")
		.substring(0, 2)
		.toUpperCase();
});

// Manager info - placeholder until we fetch from HRMS
const managerName = computed(() => {
	return "Not Assigned";
});

const managerDesignation = computed(() => {
	return "Manager";
});

const managerInitials = computed(() => {
	return managerName.value
		.split(" ")
		.map((n) => n[0])
		.join("")
		.substring(0, 2)
		.toUpperCase();
});

// Payroll info
const payslipMonth = computed(() => {
	const slip = payrollStore.latestSalarySlip;
	if (slip) {
		const date = new Date(slip.posting_date || slip.start_date);
		return date.toLocaleDateString("en-US", { month: "short", year: "numeric" });
	}
	return "No Payslip";
});

const payslipStatus = computed(() => {
	const slip = payrollStore.latestSalarySlip;
	if (slip && slip.docstatus === 1) {
		return "Paid";
	}
	return null;
});

// Shift info
const shiftLabel = computed(() => {
	if (attendance.roster?.has_roster) {
		return attendance.roster.shift_name || "Current Shift";
	}
	const hours = attendance.workingHoursTarget || 8;
	return `${hours}h Shift`;
});

// Timer color based on hours worked
const getTimerColor = computed(() => {
	if (!attendance.isCheckedIn) return "text-white/20";
	const target = attendance.workingHoursTarget || 8;
	const worked = attendance.totalHoursToday || 0;
	return worked >= target ? "text-green-500" : "text-red-500";
});

const getDotColor = computed(() => {
	const target = attendance.workingHoursTarget || 8;
	const worked = attendance.totalHoursToday || 0;
	return worked >= target ? "bg-green-500" : "bg-red-500";
});

// Recent activity from check-in history
const recentActivity = computed(() => {
	if (!attendance.todayStatus?.logs) return [];

	return attendance.todayStatus.logs
		.map((log, index) => ({
			id: index,
			title: log.log_type === "IN" ? "Clocked In" : "Clocked Out",
			time: formatTime(log.time),
			type: log.log_type === "IN" ? "info" : "clock-out",
			icon: log.log_type === "IN" ? "login" : "check_circle",
		}))
		.slice(0, 5);
});

function getActivityIconClass(type) {
	return type === "clock-out"
		? "border-primary/50 text-primary"
		: "border-white/10 text-white/40";
}

// Clock in/out handlers
async function handleClockIn() {
	const employeeId = employeeStore.employee?.employee_id;
	if (!employeeId) return;

	try {
		// Get location if available
		let latitude = null;
		let longitude = null;

		if (navigator.geolocation) {
			try {
				const position = await new Promise((resolve, reject) => {
					navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 5000 });
				});
				latitude = position.coords.latitude;
				longitude = position.coords.longitude;
			} catch (e) {
				console.log("Location not available");
			}
		}

		await attendance.clockIn(employeeId, latitude, longitude);
		startTimer();
	} catch (error) {
		console.error("Clock in failed:", error);
	}
}

async function handleClockOut() {
	const employeeId = employeeStore.employee?.employee_id;
	if (!employeeId) return;

	try {
		let latitude = null;
		let longitude = null;

		if (navigator.geolocation) {
			try {
				const position = await new Promise((resolve, reject) => {
					navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 5000 });
				});
				latitude = position.coords.latitude;
				longitude = position.coords.longitude;
			} catch (e) {
				console.log("Location not available");
			}
		}

		await attendance.clockOut(employeeId, latitude, longitude);
		stopTimer();
	} catch (error) {
		console.error("Clock out failed:", error);
	}
}

// Timer functions
function startTimer() {
	if (timerInterval) clearInterval(timerInterval);

	let seconds = Math.floor((attendance.totalHoursToday || 0) * 3600);
	updateDisplayTime(seconds);

	timerInterval = setInterval(() => {
		seconds++;
		updateDisplayTime(seconds);
	}, 1000);
}

function stopTimer() {
	if (timerInterval) {
		clearInterval(timerInterval);
		timerInterval = null;
	}
}

function updateDisplayTime(totalSeconds) {
	const h = Math.floor(totalSeconds / 3600)
		.toString()
		.padStart(2, "0");
	const m = Math.floor((totalSeconds % 3600) / 60)
		.toString()
		.padStart(2, "0");
	const s = (totalSeconds % 60).toString().padStart(2, "0");
	displayTime.value = `${h}:${m}:${s}`;
}

// Todo functions
async function addTodo() {
	if (!newTodoText.value.trim()) return;

	await tasksStore.createTodo(newTodoText.value.trim());
	newTodoText.value = "";
	showAddTodo.value = false;
}

async function toggleTodo(todoId, currentStatus) {
	await tasksStore.toggleTodo(todoId, currentStatus);
}

// Utility functions
function formatDate(dateStr) {
	if (!dateStr) return "";
	const date = new Date(dateStr);
	return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function formatTime(timeStr) {
	if (!timeStr) return "";
	const date = new Date(timeStr);
	return date.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" });
}

// Initialize
onMounted(async () => {
	await employeeStore.init();
	const employeeId = employeeStore.employee?.employee_id;

	if (employeeId) {
		attendance.init(employeeId);
		tasksStore.init();
		payrollStore.init();
	}

	// Start timer if already checked in
	if (attendance.isCheckedIn) {
		startTimer();
	}
});

onUnmounted(() => {
	stopTimer();
});
</script>
