<template>
	<div class="h-full">
		<!-- Mobile Layout (sm and below) -->
		<div class="sm:hidden h-full overflow-y-auto custom-scrollbar p-3 space-y-3">
			<!-- Mobile Clock Section -->
			<div class="glass-card rounded-2xl p-4 border border-white/5">
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
					<div class="flex gap-3 mt-4 w-full px-2">
						<button
							@click="handleClockIn"
							:disabled="attendance.isCheckedIn || attendance.loading"
							class="flex-1 h-11 rounded-xl flex items-center justify-center gap-2 font-bold text-xs uppercase transition-all"
							:class="[
								!attendance.isCheckedIn
									? 'bg-primary text-black hover:bg-yellow-400'
									: 'bg-white/5 text-white/20 cursor-not-allowed',
							]"
						>
							<span v-if="attendance.loading" class="animate-spin text-sm">rotate_right</span>
							<span v-else>Clock In</span>
						</button>
						<button
							@click="handleClockOut"
							:disabled="!attendance.isCheckedIn || attendance.loading"
							class="flex-1 h-11 rounded-xl flex items-center justify-center gap-2 font-bold text-xs uppercase transition-all"
							:class="[
								attendance.isCheckedIn
									? 'bg-white/5 border border-white/10 text-white/80 hover:bg-white/10'
									: 'bg-white/5 text-white/20 cursor-not-allowed',
							]"
						>
							<span v-if="attendance.loading" class="animate-spin text-sm">rotate_right</span>
							<span v-else>Clock Out</span>
						</button>
					</div>
				</div>
			</div>

			<!-- Mobile Profile Cards -->
			<div class="grid grid-cols-2 gap-2">
				<div class="glass-card rounded-xl p-3 border border-white/5">
					<p class="text-[8px] text-white/30 uppercase tracking-widest mb-1">Profile</p>
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
				<div class="glass-card rounded-xl p-3 border border-white/5">
					<p class="text-[8px] text-white/30 uppercase tracking-widest mb-1">Manager</p>
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
				<div class="glass-card rounded-xl p-3 border border-white/5 text-center">
					<p class="text-lg font-bold font-mono text-white">{{ totalHoursMobile }}</p>
					<p class="text-[8px] text-white/30 uppercase">Hours</p>
				</div>
				<div class="glass-card rounded-xl p-3 border border-white/5 text-center">
					<p class="text-lg font-bold font-mono text-emerald-400">{{ tasksStore.openTodos.length }}</p>
					<p class="text-[8px] text-white/30 uppercase">Tasks</p>
				</div>
				<div class="glass-card rounded-xl p-3 border border-white/5 text-center">
					<p class="text-lg font-bold font-mono text-primary">{{ payslipStatus || '—' }}</p>
					<p class="text-[8px] text-white/30 uppercase">Payroll</p>
				</div>
			</div>

			<!-- Mobile Tasks -->
			<div class="glass-card rounded-2xl p-4 border border-white/5">
				<div class="flex items-center justify-between mb-3">
					<h3 class="font-bold text-sm text-white">Priority Tasks</h3>
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
			<div class="glass-card rounded-2xl p-4 border border-white/5">
				<h3 class="font-bold text-sm text-white mb-3">Recent Activity</h3>
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

		<!-- Tablet Layout (sm to lg) -->
		<div class="hidden sm:block lg:hidden h-full overflow-y-auto custom-scrollbar p-4">
			<div class="grid grid-cols-2 gap-4 h-full">
				<!-- Left Column -->
				<div class="space-y-4 overflow-y-auto custom-scrollbar pr-2">
					<!-- Clock Section -->
					<div class="glass-card rounded-2xl p-6 border border-white/5">
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
							<div class="flex gap-3 mt-4 w-full max-w-xs">
								<button
									@click="handleClockIn"
									:disabled="attendance.isCheckedIn || attendance.loading"
									class="flex-1 h-11 rounded-xl flex items-center justify-center gap-2 font-bold text-xs uppercase transition-all"
									:class="[
										!attendance.isCheckedIn
											? 'bg-primary text-black hover:bg-yellow-400 shadow-[0_0_20px_rgba(252,211,77,0.2)]'
											: 'bg-white/5 text-white/20 cursor-not-allowed',
									]"
								>
									<span v-if="attendance.loading" class="animate-spin text-sm">rotate_right</span>
									<span v-else>Clock In</span>
								</button>
								<button
									@click="handleClockOut"
									:disabled="!attendance.isCheckedIn || attendance.loading"
									class="flex-1 h-11 rounded-xl flex items-center justify-center gap-2 font-bold text-xs uppercase transition-all"
									:class="[
										attendance.isCheckedIn
											? 'bg-white/5 border border-white/10 text-white/80 hover:bg-white/10'
											: 'bg-white/5 text-white/20 cursor-not-allowed',
									]"
								>
									<span v-if="attendance.loading" class="animate-spin text-sm">rotate_right</span>
									<span v-else>Clock Out</span>
								</button>
							</div>
						</div>
					</div>

					<!-- Profile Cards -->
					<div class="grid grid-cols-2 gap-3">
						<div class="glass-card rounded-xl p-4 border border-white/5">
							<p class="text-[8px] text-white/30 uppercase tracking-widest mb-2">Profile</p>
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
						<div class="glass-card rounded-xl p-4 border border-white/5">
							<p class="text-[8px] text-white/30 uppercase tracking-widest mb-2">Manager</p>
							<div class="flex items-center gap-2">
								<div class="w-9 h-9 rounded-full bg-blue-500/10 flex items-center justify-center text-blue-400 font-bold text-[10px] uppercase">
									{{ managerInitials }}
								</div>
								<p class="text-[11px] font-bold text-white truncate">{{ managerName }}</p>
							</div>
						</div>
					</div>

					<!-- Payroll Card -->
					<div class="glass-card rounded-xl p-4 border border-white/5">
						<div class="flex items-center justify-between">
							<div>
								<p class="text-[8px] text-white/30 uppercase tracking-widest mb-1">Payroll</p>
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

				<!-- Right Column -->
				<div class="space-y-4 overflow-y-auto custom-scrollbar pl-2">
					<!-- Tasks -->
					<div class="glass-card rounded-2xl p-5 border border-white/5 flex-1">
						<div class="flex items-center justify-between mb-4">
							<h3 class="font-bold text-base text-white">Priority Tasks</h3>
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
					<div class="glass-card rounded-2xl p-5 border border-white/5 flex-1">
						<h3 class="font-bold text-base text-white mb-4">Activity Stream</h3>
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
			</div>
		</div>

		<!-- Desktop Layout (lg and above) - Original Splitpanes -->
		<div class="hidden lg:block max-w-7xl mx-auto h-[calc(100vh-8rem)] splitpanes-dashboard">
			<splitpanes class="default-theme" @resize="onMainResize">
				<!-- Left Column: Clock & Bottom Widgets -->
				<pane :size="66" min-size="40" class="pr-2 bg-transparent overflow-hidden">
					<splitpanes horizontal class="default-theme" @resize="onLeftResize">
						<!-- Clock Section -->
						<pane :size="75" class="pb-2 bg-transparent overflow-hidden">
							<div
								class="flex-1 flex flex-col items-center justify-center py-2 glass-card rounded-[2.5rem] border border-white/5 relative bg-gradient-to-b from-white/5 to-transparent overflow-hidden h-full"
							>
								<!-- Background decorative elements -->
								<div
									class="absolute top-0 left-0 w-full h-full diamond-pattern opacity-10 pointer-events-none rounded-[2.5rem] overflow-hidden"
								></div>
								<div
									class="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,_rgba(252,211,77,0.05)_0%,_transparent_50%)] pointer-events-none rounded-[2.5rem]"
								></div>
								<div
									class="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/20 pointer-events-none rounded-[2.5rem]"
								></div>

								<div
									class="relative group z-10 scale-[0.85] lg:scale-100 flex-1 flex flex-col justify-center w-full items-center"
								>
									<!-- Outer Bezel -->
									<div
										class="w-[340px] h-[340px] lg:w-[380px] lg:h-[380px] rounded-full metallic-bezel border-[4px] border-[#222] flex items-center justify-center relative p-1 shadow-[0_0_80px_rgba(0,0,0,0.6)]"
									>
										<!-- Glowing Border Ring -->
										<div
											class="absolute inset-0 rounded-full border border-primary/10 shadow-[0_0_40px_rgba(252,211,77,0.05)]"
										></div>

										<!-- Inner Bezel Detail -->
										<div
											class="w-full h-full rounded-full border-[10px] border-[#0a0c1a] shadow-inner flex items-center justify-center relative bg-[#05070a]"
										>
											<!-- Digital Face -->
											<div
												class="w-full h-full rounded-full flex flex-col items-center justify-center relative overflow-hidden bg-[radial-gradient(circle_at_center,_#121520_0%,_#05070a_70%)]"
											>
												<!-- Subtle grid/texture on face -->
												<div
													class="absolute inset-0 opacity-5"
													style="
														background-image: radial-gradient(
															#fff 1px,
															transparent 1px
														);
														background-size: 24px 24px;
													"
												></div>
												<div
													class="absolute top-[22%] text-[9px] text-white/20 tracking-[0.5em] font-bold uppercase font-display"
												>
													{{ shiftLabel }}
												</div>

												<!-- Huge Timer -->
												<div
													class="text-[3.5rem] lg:text-[4.5rem] leading-none font-mono font-bold tracking-tighter mt-2 transition-colors duration-500 z-10 drop-shadow-2xl tabular-nums"
													:class="getTimerColor"
												>
													{{ displayTime }}
												</div>

												<!-- Active Indicators -->
												<div
													class="absolute bottom-[22%] flex gap-2.5"
													v-if="attendance.isCheckedIn"
												>
													<span
														class="w-2 h-2 rounded-full animate-pulse shadow-[0_0_10px_currentColor] bg-primary"
													></span>
													<span
														class="w-2 h-2 rounded-full opacity-20 bg-primary"
													></span>
													<span
														class="w-2 h-2 rounded-full opacity-10 bg-primary"
													></span>
												</div>
											</div>
										</div>
									</div>
								</div>

								<!-- Buttons -->
								<div class="pb-8 flex gap-4 w-full max-w-sm z-10 px-4">
									<button
										@click="handleClockIn"
										:disabled="attendance.isCheckedIn || attendance.loading"
										class="flex-1 h-12 rounded-xl flex items-center justify-center gap-2 transition-all relative font-bold tracking-widest text-xs uppercase"
										:class="[
											!attendance.isCheckedIn
												? 'bg-primary text-black hover:bg-yellow-400 hover:scale-[1.02] shadow-[0_0_30px_rgba(252,211,77,0.2)]'
												: 'bg-white/5 border border-white/5 text-white/10 cursor-not-allowed',
										]"
									>
										<span v-if="attendance.loading" class="animate-spin text-sm"
											>rotate_right</span
										>
										<span v-else>Clock In</span>
									</button>

									<button
										@click="handleClockOut"
										:disabled="!attendance.isCheckedIn || attendance.loading"
										class="flex-1 h-12 rounded-xl flex items-center justify-center gap-2 transition-all relative font-bold tracking-widest text-xs uppercase"
										:class="[
											attendance.isCheckedIn
												? 'bg-white/5 border border-white/10 text-white/80 hover:bg-white/10 hover:border-red-500/50 hover:text-red-400 shadow-lg'
												: 'bg-white/5 border border-white/5 text-white/10 cursor-not-allowed',
										]"
									>
										<span v-if="attendance.loading" class="animate-spin text-sm"
											>rotate_right</span
										>
										<span v-else>Clock Out</span>
									</button>
								</div>
							</div>
						</pane>

						<!-- Bottom Info Row -->
						<pane :size="25" min-size="15" class="pt-2 bg-transparent overflow-hidden">
							<splitpanes class="default-theme">
								<!-- Profile -->
								<pane :size="33.3" class="pr-2 bg-transparent overflow-hidden">
									<div
										class="glass-card rounded-[1.5rem] p-5 border border-white/5 flex flex-col justify-between relative overflow-hidden group hover:border-white/10 transition-colors h-full"
									>
										<div
											class="absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity"
										>
											<span class="material-symbols-outlined text-5xl"
												>badge</span
											>
										</div>
										<div>
											<p
												class="text-[9px] text-white/30 font-bold uppercase tracking-widest mb-2"
											>
												My Profile
											</p>
											<div class="flex items-center gap-3 mt-1">
												<div
													class="w-10 h-10 rounded-full bg-gradient-to-br from-primary/80 to-amber-600 flex items-center justify-center text-black font-bold text-sm shadow-lg shadow-primary/10 shrink-0"
												>
													{{ userInitials }}
												</div>
												<div class="min-w-0">
													<p
														class="text-xs font-bold text-white leading-tight truncate"
													>
														{{ employeeName }}
													</p>
													<p class="text-[9px] text-primary mt-1 truncate">
														{{ employeeDesignation }}
													</p>
												</div>
											</div>
										</div>
										<button
											class="mt-3 py-2 px-3 bg-white/5 hover:bg-white/10 rounded-lg text-[9px] font-bold text-white/70 border border-white/5 flex items-center gap-2 w-full justify-center transition-all"
										>
											<span class="material-symbols-outlined text-[14px]"
												>account_box</span
											>
											Employee Settings
										</button>
									</div>
								</pane>

								<!-- Reporting Manager -->
								<pane :size="33.4" class="px-2 bg-transparent overflow-hidden">
									<div
										class="glass-card rounded-[1.5rem] p-5 border border-white/5 flex flex-col justify-between relative overflow-hidden group hover:border-white/10 transition-colors h-full"
									>
										<div
											class="absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity"
										>
											<span class="material-symbols-outlined text-5xl"
												>supervisor_account</span
											>
										</div>
										<div>
											<p
												class="text-[9px] text-white/30 font-bold uppercase tracking-widest mb-2"
											>
												Direct Manager
											</p>
											<div class="flex items-center gap-3 mt-1">
												<div
													class="w-10 h-10 rounded-full bg-blue-500/10 flex items-center justify-center text-blue-400 font-bold text-xs ring-1 ring-blue-500/20 shrink-0 uppercase"
												>
													{{ managerInitials }}
												</div>
												<div class="min-w-0">
													<p class="text-xs font-bold text-white truncate">
														{{ managerName }}
													</p>
													<p class="text-[9px] text-white/40 truncate mt-1">
														Supervisory Role
													</p>
												</div>
											</div>
										</div>
										<button
											class="mt-3 py-2 px-3 bg-white/5 hover:bg-white/10 rounded-lg text-[9px] font-bold text-white/50 border border-white/5 transition-all w-full"
										>
											View Management
										</button>
									</div>
								</pane>

								<!-- Payslip -->
								<pane :size="33.3" class="pl-2 bg-transparent overflow-hidden">
									<div
										class="glass-card rounded-[1.5rem] p-5 border border-white/5 flex flex-col justify-between relative overflow-hidden group hover:border-white/10 transition-colors h-full"
									>
										<div
											class="absolute top-0 right-0 p-3 opacity-5 group-hover:opacity-10 transition-opacity"
										>
											<span class="material-symbols-outlined text-5xl"
												>payments</span
											>
										</div>
										<div>
											<p
												class="text-[9px] text-white/30 font-bold uppercase tracking-widest mb-2"
											>
												My Payroll
											</p>
											<p class="text-sm font-bold text-white truncate">
												{{ payslipMonth }}
											</p>
											<div
												v-if="payslipStatus"
												class="flex items-center gap-1.5 mt-2"
											>
												<span
													class="w-1.5 h-1.5 rounded-full bg-emerald-400"
												></span>
												<span
													class="text-[9px] text-emerald-400/80 font-bold uppercase tracking-wider"
													>{{ payslipStatus }}</span
												>
											</div>
											<p v-else class="text-[9px] text-white/30 mt-2 italic">
												Processing...
											</p>
										</div>
										<router-link to="/payroll" class="block mt-3 shrink-0">
											<button
												class="w-full py-2 px-3 bg-primary/5 hover:bg-primary/10 rounded-lg text-[9px] font-bold text-primary/80 border border-primary/10 flex items-center justify-center gap-2 transition-all"
											>
												<span class="material-symbols-outlined text-[14px]"
													>receipt_long</span
												>
												Salary History
											</button>
										</router-link>
									</div>
								</pane>
							</splitpanes>
						</pane>
					</splitpanes>
				</pane>

				<!-- Right Column: Activity / Todos -->
				<pane :size="34" min-size="20" class="pl-2 bg-transparent overflow-hidden">
					<splitpanes horizontal class="default-theme" @resize="onRightResize">
						<!-- Activity -->
						<pane :size="50" class="pb-2 bg-transparent overflow-hidden">
							<div
								class="glass-card rounded-[2.5rem] p-7 h-full border border-white/5 flex flex-col bg-white/[0.02]"
							>
								<div class="flex items-center justify-between mb-6">
									<div>
										<h3 class="font-bold text-lg text-white font-display">
											Activity Stream
										</h3>
										<p
											class="text-[9px] text-white/20 uppercase tracking-widest mt-1"
										>
											Real-time alerts
										</p>
									</div>
									<div
										class="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center"
									>
										<span class="material-symbols-outlined text-white/30 text-base"
											>notifications</span
										>
									</div>
								</div>
								<div class="flex-1 overflow-y-auto custom-scrollbar space-y-5 pr-2">
									<div
										v-if="recentActivity.length === 0"
										class="text-center text-white/20 py-12"
									>
										<span class="material-symbols-outlined text-4xl mb-3 opacity-20"
											>history</span
										>
										<p class="text-xs">Initial scan complete. No logs found.</p>
									</div>
									<div
										v-for="log in recentActivity"
										:key="log.id"
										class="flex gap-4 relative group"
									>
										<div
											class="w-9 h-9 rounded-xl flex items-center justify-center shrink-0 border bg-black/40 backdrop-blur-md transition-all group-hover:border-primary/30"
											:class="getActivityIconClass(log.type)"
										>
											<span class="material-symbols-outlined text-lg">{{
												log.icon
											}}</span>
										</div>
										<div class="min-w-0">
											<p
												class="text-[11px] font-bold text-white transition-colors group-hover:text-primary leading-tight"
											>
												{{ log.title }}
											</p>
											<p
												class="text-[9px] text-white/30 mt-1 font-mono uppercase"
											>
												{{ log.time }}
											</p>
										</div>
									</div>
								</div>
							</div>
						</pane>

						<!-- Todos -->
						<pane :size="50" class="pt-2 bg-transparent overflow-hidden">
							<div
								class="glass-card rounded-[2.5rem] p-7 h-full border border-white/5 flex flex-col bg-white/[0.02]"
							>
								<div class="flex items-center justify-between mb-6">
									<div>
										<h3 class="font-bold text-lg text-white font-display">
											Priority Tasks
										</h3>
										<p
											class="text-[9px] text-white/20 uppercase tracking-widest mt-1"
										>
											Personal Board
										</p>
									</div>
									<button
										@click="showAddTodo = true"
										class="w-8 h-8 rounded-xl bg-primary text-black hover:bg-yellow-400 flex items-center justify-center transition-all shadow-lg shadow-primary/10"
									>
										<span class="material-symbols-outlined text-lg font-bold"
											>add</span
										>
									</button>
								</div>
								<div class="flex-1 overflow-y-auto custom-scrollbar space-y-3 pr-2">
									<div
										v-if="sortedOpenTodos.length === 0"
										class="text-center text-white/20 py-12"
									>
										<div
											class="w-14 h-14 rounded-full border border-white/5 flex items-center justify-center mx-auto mb-4 bg-white/5"
										>
											<span class="material-symbols-outlined text-2xl opacity-30"
												>check_circle</span
											>
										</div>
										<p class="text-xs">Zero tasks remaining for today</p>
									</div>
									<div
										v-for="todo in sortedOpenTodos"
										:key="todo.id"
										@click="toggleTodo(todo.id, todo.status)"
										class="group flex items-center gap-4 p-4 rounded-2xl bg-white/[0.03] hover:bg-white/[0.06] transition-all border border-white/5 cursor-pointer"
									>
										<div
											class="w-5 h-5 rounded-md border-2 border-white/10 flex items-center justify-center group-hover:border-primary transition-all bg-black/20"
										>
											<span
												class="material-symbols-outlined text-[14px] text-transparent group-hover:text-primary"
												>done</span
											>
										</div>
										<div class="flex-1 min-w-0">
											<p
												class="text-xs font-bold text-white group-hover:text-primary/90 transition-colors truncate"
											>
												{{ todo.description }}
											</p>
											<div class="flex items-center gap-3 mt-1.5">
												<span
													class="text-[9px] text-white/30 flex items-center gap-1 font-mono uppercase"
												>
													<span class="material-symbols-outlined text-[10px]"
														>calendar_today</span
													>
													{{ formatDate(todo.date) }}
												</span>
												<span
													class="text-[8px] font-black uppercase tracking-widest px-1.5 py-0.5 rounded"
													:class="{
														'bg-red-500/15 text-red-400': todo.priority === 'High',
														'bg-amber-500/15 text-amber-400': todo.priority === 'Medium',
														'bg-blue-500/15 text-blue-400': todo.priority === 'Low'
													}"
												>
													{{ todo.priority }}
												</span>
											</div>
										</div>
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
let timerInterval = null;

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

// Splitpanes resize sync (optional cross resize support)
function onMainResize(panes) {
	// console.log('Main Resize', panes)
}
function onLeftResize(panes) {
	// console.log('Left Column Resize', panes)
}
function onRightResize(panes) {
	// console.log('Right Column Resize', panes)
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
		await attendance.clockIn(employeeId, latitude, longitude);
		startTimer();
	} catch (error) {
		console.error("Clock in failed:", error);
	}
}

async function handleClockOut() {
	const employeeId = employeeStore.employee?.name;
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
		attendance.init(employeeId);
		tasksStore.init();
		payrollStore.init();
	}
	if (attendance.isCheckedIn) {
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
