<template>
	<div class="h-full overflow-hidden">
		<!-- Mobile Layout (md and below) -->
		<div class="md:hidden h-full overflow-y-auto custom-scrollbar p-3 flex flex-col gap-3">
			<!-- Mobile Clock Section -->
			<div class="premium-card">
				<div class="flex flex-col items-center py-4">
					<!-- Mini Clock -->
					<div class="w-48 h-48 rounded-full metallic-bezel border-[3px] border-[#222] flex items-center justify-center p-1 shadow-[0_0_40px_rgba(0,0,0,0.4)]">
						<div class="w-full h-full rounded-full border-[6px] border-[#0a0c1a] flex items-center justify-center bg-[#05070a]">
							<div class="text-center">
								<div
									class="text-3xl font-mono font-bold tracking-tight transition-colors"
									:class="getTimerColor"
								>
									{{ displayTime }}
								</div>
								<div class="text-[8px] text-white/30 uppercase tracking-widest mt-1">
									{{ shiftLabel }}
								</div>
							</div>
						</div>
					</div>

					<!-- Mobile Clock Buttons -->
					<div class="grid grid-cols-2 gap-2 mt-4 w-full px-2">
						<button
							@click="handleClockIn()"
							:disabled="attendance.isCheckedIn || attendance.loading"
							class="h-11 rounded-xl flex items-center justify-center gap-2 font-bold text-[10px] uppercase transition-colors shadow-lg"
							:class="[
								!attendance.isCheckedIn
									? 'bg-primary text-black hover:bg-yellow-400 shadow-primary/20'
									: 'bg-white/5 border border-white/10 text-white/20 cursor-not-allowed',
							]"
						>
							Clock In
						</button>
						<button
							@click="handleClockOut()"
							:disabled="!attendance.isCheckedIn || attendance.loading"
							class="h-11 rounded-xl flex items-center justify-center gap-2 font-bold text-[10px] uppercase transition-colors shadow-lg"
							:class="[
								attendance.isCheckedIn
									? 'bg-red-500/20 border border-red-500/30 text-red-500 hover:bg-red-500/30 shadow-red-500/10'
									: 'bg-white/5 border border-white/10 text-white/20 cursor-not-allowed',
							]"
						>
							Clock Out
						</button>
						<button
							@click="handleBreak"
							:disabled="!attendance.isCheckedIn || attendance.loading"
							class="col-span-2 h-11 rounded-xl flex items-center justify-center gap-2 font-bold text-[10px] uppercase transition-colors"
							:class="isOnBreak ? 'bg-primary text-black shadow-primary/20' : 'bg-white/5 border border-white/10 text-white/80 hover:bg-white/10 disabled:opacity-30'"
						>
							<span v-if="attendance.loading" class="text-sm">...</span>
							<span v-else>{{ isOnBreak ? 'End Break' : 'Break' }}</span>
						</button>
					</div>
				</div>
			</div>

			<!-- Mobile Profile Cards -->
			<div class="grid grid-cols-2 gap-2">
				<div class="premium-card !p-3">
					<p class="status-label !mb-1">Profile</p>
					<div class="flex items-center gap-2">
						<div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary/80 to-amber-600 flex items-center justify-center text-black font-bold text-xs">
							{{ userInitials }}
						</div>
						<div class="min-w-0">
							<p class="text-[10px] font-bold text-white truncate">{{ employeeName }}</p>
							<p class="text-[8px] text-primary truncate">{{ employeeDesignation }}</p>
						</div>
					</div>
				</div>
				<div class="premium-card !p-3">
					<p class="status-label !mb-1">Manager</p>
					<div class="flex items-center gap-2">
						<div class="w-8 h-8 rounded-full bg-blue-500/10 flex items-center justify-center text-blue-400 font-bold text-[10px] uppercase">
							{{ managerInitials }}
						</div>
						<p class="text-[10px] font-bold text-white truncate">{{ managerName }}</p>
					</div>
				</div>
			</div>

			<!-- Mobile Quick Stats -->
			<div class="grid grid-cols-3 gap-2">
				<div class="premium-card !p-3 flex flex-col items-center">
					<p class="text-lg font-bold font-mono text-gray-900 dark:text-white">{{ totalHoursMobile }}</p>
					<p class="status-label !mb-0 text-[8px]">Hours</p>
				</div>
				<div class="premium-card !p-3 flex flex-col items-center">
					<p class="text-lg font-bold font-mono text-emerald-600 dark:text-emerald-400">{{ tasksStore.openTodos.length }}</p>
					<p class="status-label !mb-0 text-[8px]">Tasks</p>
				</div>
				<div class="premium-card !p-3 flex flex-col items-center">
					<p class="text-lg font-bold font-mono text-primary">{{ payslipStatus || '—' }}</p>
					<p class="status-label !mb-0 text-[8px]">Payroll</p>
				</div>
			</div>

			<!-- Mobile Tasks -->
			<div class="premium-card">
				<div class="flex items-center justify-between mb-3">
					<h3 class="premium-title !text-sm">Priority Tasks</h3>
					<button
						@click="showAddTodo = true"
						class="w-7 h-7 rounded-lg bg-primary text-black flex items-center justify-center"
					>
						<span class="material-symbols-outlined text-sm font-bold">add</span>
					</button>
				</div>
				<div class="space-y-2">
					<div v-if="sortedOpenTodos.length === 0" class="text-center py-6">
						<p class="text-xs text-white/30">No tasks</p>
					</div>
					<div
						v-for="todo in sortedOpenTodos.slice(0, 3)"
						:key="todo.id"
						@click="toggleTodo(todo.id, todo.status)"
						class="flex items-center gap-3 p-3 rounded-xl bg-white/[0.03] border border-white/5"
					>
						<div class="w-4 h-4 rounded border border-white/20"></div>
						<div class="flex-1 min-w-0">
							<p class="text-xs text-white truncate">{{ todo.description }}</p>
						</div>
						<span
							class="text-[8px] font-bold uppercase px-1.5 py-0.5 rounded"
							:class="{
								'bg-red-500/15 text-red-400': todo.priority === 'High',
								'bg-amber-500/15 text-amber-400': todo.priority === 'Medium',
								'bg-blue-500/15 text-blue-400': todo.priority === 'Low'
							}"
						>{{ todo.priority }}</span>
					</div>
				</div>
			</div>

			<!-- Mobile Activity -->
			<div class="premium-card">
				<h3 class="premium-title !text-sm mb-3">Recent Activity</h3>
				<div class="space-y-2">
					<div v-if="recentActivity.length === 0" class="text-center py-4">
						<p class="text-xs text-white/30">No activity</p>
					</div>
					<div
						v-for="log in recentActivity.slice(0, 3)"
						:key="log.name"
						class="flex items-center gap-3 p-2 rounded-lg bg-white/[0.02]"
					>
						<div class="w-8 h-8 rounded-full flex items-center justify-center"
							:class="getLogStyle(log.log_type).bg">
							<span class="material-symbols-outlined text-sm"
								:class="getLogStyle(log.log_type).text">
								{{ getLogStyle(log.log_type).icon }}
							</span>
						</div>
						<div class="flex-1 min-w-0">
							<p class="text-[10px] font-bold text-white">{{ getLogStyle(log.log_type).label }}</p>
							<p class="text-[9px] text-white/40">{{ formatDateTime(log.time) }}</p>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Tablet Layout (md to xl) -->
		<div class="hidden md:block xl:hidden h-full overflow-y-auto custom-scrollbar p-4">
			<div class="grid grid-cols-2 gap-4 h-full auto-rows-min">
				<!-- Timer spans 2 columns -->
				<div class="col-span-2">
					<!-- Clock Section -->
					<div class="premium-card">
						<div class="flex flex-col items-center py-2">
							<div class="w-56 h-56 rounded-full metallic-bezel border-[3px] border-[#222] flex items-center justify-center p-1 shadow-[0_0_50px_rgba(0,0,0,0.5)]">
								<div class="w-full h-full rounded-full border-[8px] border-[#0a0c1a] flex items-center justify-center bg-[#05070a]">
									<div class="text-center">
										<div class="text-4xl font-mono font-bold tracking-tight" :class="getTimerColor">
											{{ displayTime }}
										</div>
										<div class="text-[9px] text-white/30 uppercase tracking-widest mt-1">
											{{ shiftLabel }}
										</div>
									</div>
								</div>
							</div>
							<div class="grid grid-cols-2 gap-2 mt-4 w-full max-w-xs">
								<button
									@click="handleClockIn()"
									:disabled="attendance.isCheckedIn || attendance.loading"
									class="h-11 rounded-xl flex items-center justify-center gap-2 font-bold text-[10px] uppercase transition-all shadow-lg"
									:class="[
										!attendance.isCheckedIn
											? 'bg-primary text-black hover:bg-yellow-400 shadow-primary/20'
											: 'bg-white/5 border border-white/10 text-white/20 cursor-not-allowed',
									]"
								>
									Clock In
								</button>
								<button
									@click="handleClockOut()"
									:disabled="!attendance.isCheckedIn || attendance.loading"
									class="h-11 rounded-xl flex items-center justify-center gap-2 font-bold text-[10px] uppercase transition-all shadow-lg"
									:class="[
										attendance.isCheckedIn
											? 'bg-red-500/20 border border-red-500/30 text-red-500 hover:bg-red-500/30 shadow-red-500/10'
											: 'bg-white/5 border border-white/10 text-white/20 cursor-not-allowed',
									]"
								>
									Clock Out
								</button>
								<button
									@click="handleBreak"
									:disabled="!attendance.isCheckedIn || attendance.loading"
									class="col-span-2 h-11 rounded-xl flex items-center justify-center gap-2 font-bold text-[10px] uppercase transition-colors"
									:class="isOnBreak ? 'bg-primary text-black shadow-primary/20' : 'bg-white/5 border border-white/10 text-white/80 hover:bg-white/10 disabled:opacity-30'"
								>
									<span v-if="attendance.loading" class="text-sm">...</span>
									<span v-else>{{ isOnBreak ? 'End Break' : 'Break' }}</span>
								</button>
							</div>
						</div>
					</div>

					<!-- Profile Cards -->
					<div class="grid grid-cols-2 gap-3">
						<div class="premium-card !p-4">
							<p class="status-label !mb-2">Profile</p>
							<div class="flex items-center gap-2">
								<div class="w-9 h-9 rounded-full bg-gradient-to-br from-primary/80 to-amber-600 flex items-center justify-center text-black font-bold text-xs">
									{{ userInitials }}
								</div>
								<div class="min-w-0">
									<p class="text-[11px] font-bold text-white truncate">{{ employeeName }}</p>
									<p class="text-[9px] text-primary truncate">{{ employeeDesignation }}</p>
								</div>
							</div>
						</div>
						<div class="premium-card !p-4">
							<p class="status-label !mb-2">Manager</p>
							<div class="flex items-center gap-2">
								<div class="w-9 h-9 rounded-full bg-blue-500/10 flex items-center justify-center text-blue-400 font-bold text-[10px] uppercase">
									{{ managerInitials }}
								</div>
								<p class="text-[11px] font-bold text-white truncate">{{ managerName }}</p>
							</div>
						</div>
					</div>

					<!-- Payroll Card -->
					<div class="premium-card !p-4">
						<div class="flex items-center justify-between">
							<div>
								<p class="status-label !mb-1">Payroll</p>
								<p class="text-sm font-bold text-white">{{ payslipMonth }}</p>
								<span v-if="payslipStatus" class="text-[9px] text-emerald-400 font-bold uppercase">{{ payslipStatus }}</span>
							</div>
							<router-link to="/payroll">
								<button class="px-3 py-2 bg-primary/10 rounded-lg text-[9px] font-bold text-primary">
									View History
								</button>
							</router-link>
						</div>
					</div>
				</div>

				<!-- Activity & Tasks Row (2 columns) -->
				<div class="premium-card">
					<div class="flex items-center justify-between mb-4">
						<h3 class="premium-title !text-base">Priority Tasks</h3>
						<button
							@click="showAddTodo = true"
							class="w-8 h-8 rounded-lg bg-primary text-black flex items-center justify-center"
						>
							<span class="material-symbols-outlined text-base font-bold">add</span>
						</button>
					</div>
					<div class="space-y-2 max-h-[200px] overflow-y-auto custom-scrollbar pr-1">
						<div v-if="sortedOpenTodos.length === 0" class="text-center py-6">
							<p class="text-xs text-white/30">No tasks remaining</p>
						</div>
						<div
							v-for="todo in sortedOpenTodos"
							:key="todo.id"
							@click="toggleTodo(todo.id, todo.status)"
							class="flex items-center gap-3 p-3 rounded-xl bg-white/[0.03] border border-white/5 cursor-pointer hover:bg-white/[0.05] transition-colors"
						>
							<div class="w-4 h-4 rounded border border-white/20"></div>
							<div class="flex-1 min-w-0">
								<p class="text-xs text-white truncate">{{ todo.description }}</p>
							</div>
							<span
								class="text-[8px] font-bold uppercase px-1.5 py-0.5 rounded"
								:class="{
									'bg-red-500/15 text-red-400': todo.priority === 'High',
									'bg-amber-500/15 text-amber-400': todo.priority === 'Medium',
									'bg-blue-500/15 text-blue-400': todo.priority === 'Low'
								}"
							>{{ todo.priority }}</span>
						</div>
					</div>
				</div>

				<!-- Activity -->
				<div class="premium-card">
					<h3 class="premium-title !text-base mb-4">Activity Stream</h3>
					<div class="space-y-2 max-h-[200px] overflow-y-auto custom-scrollbar pr-1">
						<div v-if="recentActivity.length === 0" class="text-center py-6">
							<p class="text-xs text-white/30">No recent activity</p>
						</div>
						<div
							v-for="log in recentActivity"
							:key="log.name"
							class="flex items-center gap-3 p-2 rounded-lg bg-white/[0.02]"
						>
							<div class="w-8 h-8 rounded-full flex items-center justify-center"
								:class="getLogStyle(log.log_type).bg">
								<span class="material-symbols-outlined text-sm"
									:class="getLogStyle(log.log_type).text">
									{{ getLogStyle(log.log_type).icon }}
								</span>
							</div>
							<div class="flex-1 min-w-0">
								<p class="text-[10px] font-bold text-white">{{ getLogStyle(log.log_type).label }}</p>
								<p class="text-[9px] text-white/40">{{ formatDateTime(log.time) }}</p>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>		<!-- Desktop Layout (xl and above) - Interactive Splitpanes -->
		<div class="hidden xl:block h-full overflow-hidden p-4">
			<splitpanes class="splitpanes-dashboard" @resize="onMainResize">
				<!-- Left Column: Clock & People -->
				<pane :size="paneSizes.main[0]" min-size="25" class="pr-2 bg-transparent overflow-hidden">
					<splitpanes horizontal class="splitpanes-dashboard" @resize="onLeftResize">
						<!-- Clock Section -->
						<pane :size="paneSizes.left[0]" class="pb-2 bg-transparent overflow-hidden">
							<div class="flex-1 flex flex-col items-center justify-center py-2 premium-card relative bg-gradient-to-b from-white/5 to-transparent h-full">
								<div class="absolute top-0 left-0 w-full h-full diamond-pattern opacity-10 pointer-events-none overflow-hidden"></div>
								<div class="relative group z-10 scale-[0.8] lg:scale-90 flex-1 flex flex-col justify-center w-full items-center">
									<div class="w-[300px] h-[300px] lg:w-[340px] lg:h-[340px] rounded-full metallic-bezel border-[4px] border-[#222] flex items-center justify-center relative p-1 shadow-[0_0_80px_rgba(0,0,0,0.6)]">
										<div class="w-full h-full rounded-full border-[10px] border-[#0a0c1a] shadow-inner flex items-center justify-center relative bg-[#05070a]">
											<div class="w-full h-full rounded-full flex flex-col items-center justify-center relative overflow-hidden bg-[radial-gradient(circle_at_center,_#121520_0%,_#05070a_70%)]">
												<div class="absolute top-[22%] text-[8px] text-white/20 tracking-[0.5em] font-bold uppercase font-display">{{ shiftLabel }}</div>
												<div class="text-[3rem] lg:text-[4rem] leading-none font-mono font-bold tracking-tighter mt-2 transition-colors duration-500 z-10 drop-shadow-2xl tabular-nums" :class="getTimerColor">
													{{ displayTime }}
												</div>
												<div class="absolute bottom-[22%] flex gap-2" v-if="attendance.isCheckedIn">
													<span class="w-1.5 h-1.5 rounded-full animate-pulse bg-primary"></span>
													<span class="w-1.5 h-1.5 rounded-full opacity-20 bg-primary"></span>
												</div>
											</div>
										</div>
									</div>
								</div>
								<div class="pb-6 grid grid-cols-2 gap-2 w-full max-w-xs z-10 px-4">
									<button @click="handleClockIn()" :disabled="attendance.isCheckedIn || attendance.loading" class="h-11 rounded-xl flex items-center justify-center gap-2 transition-all relative font-bold tracking-widest text-[10px] uppercase shadow-lg" :class="[!attendance.isCheckedIn ? 'bg-primary text-black hover:bg-yellow-400 shadow-primary/20' : 'bg-white/5 border border-white/10 text-white/20 cursor-not-allowed']">
										Clock In
									</button>
									<button @click="handleClockOut()" :disabled="!attendance.isCheckedIn || attendance.loading" class="h-11 rounded-xl flex items-center justify-center gap-2 transition-all relative font-bold tracking-widest text-[10px] uppercase shadow-lg" :class="[attendance.isCheckedIn ? 'bg-red-500/20 border border-red-500/30 text-red-500 hover:bg-red-500/30 shadow-red-500/10' : 'bg-white/5 border border-white/10 text-white/20 cursor-not-allowed']">
										Clock Out
									</button>
									<button @click="handleBreak" :disabled="!attendance.isCheckedIn || attendance.loading" class="col-span-2 h-11 rounded-xl flex items-center justify-center gap-2 transition-all relative font-bold tracking-widest text-[10px] uppercase shadow-lg" :class="[isOnBreak ? 'bg-primary text-black hover:bg-yellow-400 shadow-primary/20' : 'bg-white/5 border border-white/10 text-white/80 hover:bg-white/10 disabled:opacity-30']">
										{{ isOnBreak ? 'End Break' : 'Break' }}
									</button>
								</div>
							</div>
						</pane>
						<!-- People Section -->
						<pane :size="paneSizes.left[1]" class="pt-2 bg-transparent overflow-hidden">
							<div class="grid grid-cols-2 gap-2 h-full">
								<div class="premium-card !p-4 flex flex-col justify-between">
									<p class="status-label">My Profile</p>
									<div class="flex items-center gap-3">
										<div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary/80 to-amber-600 flex items-center justify-center text-black font-bold text-[10px] shadow-lg">
											{{ userInitials }}
										</div>
										<p class="text-[10px] font-bold text-gray-900 dark:text-white truncate">{{ employeeName }}</p>
									</div>
								</div>
								<div class="premium-card !p-4 flex flex-col justify-between">
									<p class="status-label">Manager</p>
									<div class="flex items-center gap-3">
										<div class="w-8 h-8 rounded-full bg-blue-500/10 flex items-center justify-center text-blue-400 font-bold text-[10px] uppercase border border-blue-500/20">
											{{ managerInitials }}
										</div>
										<p class="text-[10px] font-bold text-gray-900 dark:text-white truncate">{{ managerName }}</p>
									</div>
								</div>
							</div>
						</pane>
					</splitpanes>
				</pane>

				<!-- Center Column: Roster & Payroll -->
				<pane :size="paneSizes.main[1]" min-size="30" class="px-2 bg-transparent overflow-hidden">
					<splitpanes horizontal class="splitpanes-dashboard" @resize="onCenterResize">
						<!-- Upcoming Roster -->
						<pane :size="paneSizes.center[0]" class="pb-2 bg-transparent overflow-hidden">
							<div class="premium-card !p-7 h-full flex flex-col">
								<div class="flex items-center justify-between mb-6">
									<div>
										<h3 class="premium-title !text-lg">Upcoming Roster</h3>
										<p class="premium-subtitle !text-[9px] uppercase tracking-widest mt-1">Next 5 Shifts</p>
									</div>
									<div class="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center">
										<span class="material-symbols-outlined text-gray-400 dark:text-white/30 text-base">calendar_view_week</span>
									</div>
								</div>
								<div class="space-y-2 flex-1 overflow-y-auto custom-scrollbar pr-2">
									<div v-for="roster in upcomingRoster" :key="roster.date" class="bg-white/5 p-3 rounded-xl border border-white/5 flex items-center justify-between group hover:bg-white/[0.03] transition-all">
										<div class="flex items-center gap-4">
											<div class="text-center min-w-[36px]">
												<p class="text-[9px] uppercase font-black text-white/30">{{ roster.dayShort }}</p>
												<p class="text-base font-bold text-white font-mono">{{ roster.dayNum }}</p>
											</div>
											<div class="h-8 w-px bg-white/5"></div>
											<div>
												<p class="text-[11px] font-bold text-white/90">{{ roster.shift_name }}</p>
												<p class="text-[9px] text-white/30 font-mono">{{ roster.shift_time }}</p>
											</div>
										</div>
										<div class="text-right">
											<span class="text-[8px] font-black px-2 py-0.5 rounded bg-primary/10 text-primary uppercase tracking-widest">
												{{ roster.hours }}H
											</span>
										</div>
									</div>
								</div>
							</div>
						</pane>
						<pane :size="paneSizes.center[1]" class="pt-2 bg-transparent overflow-hidden">
							<div class="premium-card !p-6 h-full flex flex-col justify-between">
								<div class="flex items-center justify-between">
									<div>
										<p class="status-label">My Payroll</p>
										<p class="text-base font-bold text-gray-900 dark:text-white">{{ payslipMonth }}</p>
										<div v-if="payslipStatus" class="flex items-center gap-1.5 mt-2">
											<span class="w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.4)]"></span>
											<span class="text-[9px] text-emerald-400 font-bold uppercase tracking-wider">{{ payslipStatus }}</span>
										</div>
									</div>
									<router-link to="/payroll">
										<button class="w-10 h-10 rounded-xl bg-white/5 hover:bg-white/10 flex items-center justify-center transition-all border border-white/5">
											<span class="material-symbols-outlined text-gray-400 dark:text-white/40 text-lg">receipt_long</span>
										</button>
									</router-link>
								</div>
								<button class="mt-4 py-2.5 bg-primary/5 hover:bg-primary/10 rounded-xl text-[10px] font-bold text-primary border border-primary/10 transition-all">
									Download Statement
								</button>
							</div>
						</pane>
					</splitpanes>
				</pane>

				<!-- Right Column: Activity / Tasks -->
				<pane :size="paneSizes.main[2]" min-size="20" class="pl-2 bg-transparent overflow-hidden">
					<splitpanes horizontal class="splitpanes-dashboard" @resize="onRightResize">
						<!-- Activity -->
						<pane :size="paneSizes.right[0]" class="pb-2 bg-transparent overflow-hidden">
							<div class="premium-card !p-7 h-full flex flex-col">
								<div class="flex items-center justify-between mb-6">
									<div>
										<h3 class="premium-title !text-lg">Activity Stream</h3>
										<p class="premium-subtitle !text-[9px] uppercase tracking-widest mt-1">Recent Logs</p>
									</div>
									<div class="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center">
										<span class="material-symbols-outlined text-gray-400 dark:text-white/30 text-base">notifications</span>
									</div>
								</div>
								<div class="flex-1 overflow-y-auto custom-scrollbar space-y-4 pr-2">
									<div v-for="log in recentActivity" :key="log.id" class="flex items-center gap-3 group">
										<div class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 border bg-black/20 border-white/5 transition-all group-hover:border-primary/30" :class="getActivityIconClass(log.type)">
											<span class="material-symbols-outlined text-base">{{ log.icon }}</span>
										</div>
										<div class="min-w-0">
											<p class="text-[10px] font-bold text-gray-900 dark:text-white/90 group-hover:text-primary transition-colors truncate">{{ log.title }}</p>
											<p class="text-[8px] text-white/30 font-mono">{{ log.time }}</p>
										</div>
									</div>
								</div>
							</div>
						</pane>
						<!-- Tasks -->
						<pane :size="paneSizes.right[1]" class="pt-2 bg-transparent overflow-hidden">
							<div class="premium-card !p-7 h-full flex flex-col">
								<div class="flex items-center justify-between mb-6">
									<div>
										<h3 class="premium-title !text-lg">Priority Tasks</h3>
										<p class="premium-subtitle !text-[9px] uppercase tracking-widest mt-1">Todo List</p>
									</div>
									<button @click="showAddTodo = true" class="w-8 h-8 rounded-xl bg-primary text-black hover:bg-yellow-400 flex items-center justify-center transition-all shadow-lg shadow-primary/20">
										<span class="material-symbols-outlined text-lg font-bold">add</span>
									</button>
								</div>
								<div class="flex-1 overflow-y-auto custom-scrollbar space-y-3 pr-2">
									<div v-for="todo in sortedOpenTodos" :key="todo.id" @click="toggleTodo(todo.id, todo.status)" class="group flex items-center gap-3 p-3 rounded-xl bg-white/[0.02] hover:bg-white/[0.05] transition-all border border-white/5 cursor-pointer">
										<div class="w-4 h-4 rounded border border-white/10 group-hover:border-primary transition-all"></div>
										<p class="text-[10px] font-bold text-gray-900 dark:text-white group-hover:text-primary/90 transition-colors truncate">{{ todo.description }}</p>
									</div>
								</div>
							</div>
						</pane>
					</splitpanes>
				</pane>
			</splitpanes>
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
						class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-primary/50 mb-3"
						@keyup.enter="addTodo"
					/>
					<div class="mb-4">
						<label class="text-[10px] text-white/40 uppercase tracking-widest mb-2 block">Priority</label>
						<div class="flex gap-2">
							<button
								@click="newTodoPriority = 'Low'"
								class="flex-1 py-2 rounded-lg text-xs font-bold transition-all"
								:class="newTodoPriority === 'Low' ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30' : 'bg-white/5 text-white/40 border border-white/5'"
							>
								Low
							</button>
							<button
								@click="newTodoPriority = 'Medium'"
								class="flex-1 py-2 rounded-lg text-xs font-bold transition-all"
								:class="newTodoPriority === 'Medium' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' : 'bg-white/5 text-white/40 border border-white/5'"
							>
								Medium
							</button>
							<button
								@click="newTodoPriority = 'High'"
								class="flex-1 py-2 rounded-lg text-xs font-bold transition-all"
								:class="newTodoPriority === 'High' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 'bg-white/5 text-white/40 border border-white/5'"
							>
								High
							</button>
						</div>
					</div>
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
import { Splitpanes, Pane } from "splitpanes";
import "splitpanes/dist/splitpanes.css";

const auth = useAuthStore();
const employeeStore = useEmployeeStore();
const attendance = useAttendanceStore();
const tasksStore = useTasksStore();
const payrollStore = usePayrollStore();

const showAddTodo = ref(false);
const newTodoText = ref("");
const newTodoPriority = ref("Medium");
const displayTime = ref("00:00:00");
const isOnBreak = ref(false);
const accumulatedSeconds = ref(0);
let timerInterval = null;

// State Persistence
function saveTimerState() {
	const state = {
		isCheckedIn: attendance.isCheckedIn,
		isOnBreak: isOnBreak.value,
		accumulatedSeconds: accumulatedSeconds.value,
		lastUpdate: Date.now()
	};
	localStorage.setItem('employee_timer_state', JSON.stringify(state));
}

function loadTimerState() {
	const saved = localStorage.getItem('employee_timer_state');
	if (saved) {
		const state = JSON.parse(saved);
		// Basic validation
		if (state.isCheckedIn !== attendance.isCheckedIn) {
			localStorage.removeItem('employee_timer_state');
			return;
		}
		
		isOnBreak.value = state.isOnBreak;
		accumulatedSeconds.value = state.accumulatedSeconds;
		
		if (attendance.isCheckedIn && !isOnBreak.value) {
			// Add elapsed time since last update
			const elapsed = Math.floor((Date.now() - state.lastUpdate) / 1000);
			accumulatedSeconds.value += elapsed;
		}
		updateDisplayTime(accumulatedSeconds.value);
	}
}

// Priority order for sorting
const priorityOrder = { High: 1, Medium: 2, Low: 3 };

// Sort open todos by priority
const sortedOpenTodos = computed(() => {
	return [...tasksStore.openTodos]
		.sort((a, b) => (priorityOrder[a.priority] || 99) - (priorityOrder[b.priority] || 99))
		.slice(0, 5);
});

// Mobile computed
const totalHoursMobile = computed(() => {
	return (attendance.totalHoursToday || 0).toFixed(1);
});

// Splitpanes resize sync and persistence
const paneSizes = ref({
	main: [35, 35, 30],
	left: [70, 30],
	center: [60, 40],
	right: [50, 50],
});

function saveLayout() {
	localStorage.setItem("dashboard_layout", JSON.stringify(paneSizes.value));
}

function loadLayout() {
	const saved = localStorage.getItem("dashboard_layout");
	if (saved) {
		try {
			const parsed = JSON.parse(saved);
			if (parsed.main && parsed.left && parsed.right) {
				paneSizes.value = parsed;
			}
		} catch (e) {
			console.error("Failed to load layout:", e);
		}
	}
}

function onMainResize(panes) {
	paneSizes.value.main = panes.map((p) => p.size);
	saveLayout();
}
function onLeftResize(panes) {
	paneSizes.value.left = panes.map((p) => p.size);
	saveLayout();
}
function onCenterResize(panes) {
	paneSizes.value.center = panes.map((p) => p.size);
	saveLayout();
}
function onRightResize(panes) {
	paneSizes.value.right = panes.map((p) => p.size);
	saveLayout();
}

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

// Manager info
const managerName = computed(() => {
	return employeeStore.employee?.reports_to || "Not Assigned";
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
	return worked >= target ? "text-green-500" : "text-amber-500";
});

const getDotColor = computed(() => {
	const target = attendance.workingHoursTarget || 8;
	const worked = attendance.totalHoursToday || 0;
	return worked >= target ? "bg-green-500" : "bg-amber-500";
});

const upcomingRoster = computed(() => {
	const days = [];
	const today = new Date();
	const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
	const dayNamesOrder = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

	for (let i = 0; i < 5; i++) {
		const d = new Date();
		d.setDate(today.getDate() + i);
		days.push({
			date: d.toISOString().split("T")[0],
			dayName: d.toLocaleDateString("en-US", { weekday: "short" }),
			dayShort: d.toLocaleDateString("en-US", { weekday: "short" }).toUpperCase(),
			dayNum: d.getDate(),
			month: monthNames[d.getMonth()],
			shift_name: attendance.roster?.shift_name || "General Shift",
			shift_time: `${attendance.roster?.start_time?.substring(0, 5) || "09:00"} - ${attendance.roster?.end_time?.substring(0, 5) || "17:00"}`,
			hours: attendance.workingHoursTarget || 8,
		});
	}
	return days;
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

function getLogStyle(logType) {
	switch (logType) {
		case "IN":
			return {
				bg: "bg-emerald-500/10",
				text: "text-emerald-400",
				icon: "login",
				label: "Clocked In",
			};
		case "OUT":
			return {
				bg: "bg-blue-500/10",
				text: "text-blue-400",
				icon: "logout",
				label: "Clocked Out",
			};
		default:
			return {
				bg: "bg-white/5",
				text: "text-white/40",
				icon: "circle",
				label: "Activity",
			};
	}
}

// Clock in/out handlers
async function handleClockIn() {
	const employeeId = employeeStore.employee?.name;
	if (!employeeId) return;
	
	// Optimistic UI update
	if (!attendance.todayStatus) attendance.todayStatus = {};
	attendance.todayStatus.checked_in = true;
	accumulatedSeconds.value = 0;
	isOnBreak.value = false;
	startTimer();
	saveTimerState();

	try {
		// Location access removed per task requirement
		await attendance.clockIn(employeeId, null, null);
	} catch (error) {
		console.error("Clock in failed:", error);
		// Revert optimistic update
		attendance.todayStatus.checked_in = false;
		stopTimer();
		localStorage.removeItem('employee_timer_state');
	}
}

async function handleClockOut() {
	const employeeId = employeeStore.employee?.name;
	if (!employeeId) return;

	// Optimistic UI update
	if (attendance.todayStatus) {
		attendance.todayStatus.checked_in = false;
	}
	stopTimer();
	localStorage.removeItem('employee_timer_state');

	try {
		// Location access removed per task requirement
		await attendance.clockOut(employeeId, null, null, "End of Shift");
	} catch (error) {
		console.error("Clock out failed:", error);
		// Revert optimistic update
		if (attendance.todayStatus) {
			attendance.todayStatus.checked_in = true;
		}
		startTimer();
	}
}

async function handleBreak() {
	const wasOnBreak = isOnBreak.value;
	isOnBreak.value = !isOnBreak.value;
	
	if (isOnBreak.value) {
		// Starting break: pause timer, create OUT checkin
		stopTimer();
		try {
			await attendance.startBreak();
		} catch (error) {
			console.error("Start break failed:", error);
			isOnBreak.value = false;
			startTimer();
		}
	} else {
		// Ending break: resume timer, create IN checkin
		startTimer();
		try {
			await attendance.endBreak();
		} catch (error) {
			console.error("End break failed:", error);
			isOnBreak.value = true;
			stopTimer();
		}
	}
	saveTimerState();
}

// Timer functions
function startTimer() {
	if (timerInterval) clearInterval(timerInterval);
	
	// Initial value from store if no accumulated seconds yet
	if (accumulatedSeconds.value === 0) {
		accumulatedSeconds.value = Math.floor((attendance.totalHoursToday || 0) * 3600);
	}
	
	updateDisplayTime(accumulatedSeconds.value);
	timerInterval = setInterval(() => {
		accumulatedSeconds.value++;
		updateDisplayTime(accumulatedSeconds.value);
		saveTimerState();
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
	await tasksStore.createTodo(newTodoText.value.trim(), null, newTodoPriority.value);
	newTodoText.value = "";
	newTodoPriority.value = "Medium";
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

// Initialize
onMounted(async () => {
	await employeeStore.init();
	const employeeId = employeeStore.employee?.name;
	if (employeeId) {
		await attendance.init(employeeId);
		tasksStore.init();
		payrollStore.init();
	}
	
	// Load saved state and layout before starting timer
	loadTimerState();
	loadLayout();
	
	if (attendance.isCheckedIn && !isOnBreak.value) {
		startTimer();
	}
});

onUnmounted(() => {
	stopTimer();
});
</script>

<style>
/* Splitpanes Theme Customization */
.splitpanes-dashboard {
	transition: opacity 0.3s;
}

.splitpanes-dashboard .splitpanes__pane {
	background-color: transparent !important;
}

.splitpanes-dashboard .splitpanes__splitter {
	background-color: transparent !important;
	border: none !important;
	position: relative;
	box-sizing: border-box;
	transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
	z-index: 20;
}

/* Hide all splitter lines completely */
.splitpanes-dashboard .splitpanes__splitter:before,
.splitpanes-dashboard .splitpanes__splitter:after {
	display: none !important;
	content: none !important;
}

.splitpanes-dashboard .splitpanes--vertical > .splitpanes__splitter {
	width: 10px;
	margin-left: -5px;
	margin-right: -5px;
	cursor: col-resize;
	border-left: none !important;
}

.splitpanes-dashboard .splitpanes--horizontal > .splitpanes__splitter {
	height: 10px;
	margin-top: -5px;
	margin-bottom: -5px;
	cursor: row-resize;
	border-top: none !important;
}

/* Custom scrollbar for activity/todos */
.custom-scrollbar::-webkit-scrollbar {
	width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
	background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
	background: rgba(255, 255, 255, 0.05);
	border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
	background: rgba(255, 255, 255, 0.1);
}

.diamond-pattern {
	background-image: radial-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px);
	background-size: 32px 32px;
}
</style>
