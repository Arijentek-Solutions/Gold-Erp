<template>
	<div class="flex flex-col gap-8">
		<!-- Stats Row -->
		<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
			<div class="glass-card p-6 rounded-2xl relative overflow-hidden group">
				<div
					class="absolute inset-0 bg-primary/5 group-hover:bg-primary/10 transition-colors"
				></div>
				<h3 class="text-xs font-bold text-white/40 uppercase mb-2 relative z-10">
					Total Hours
				</h3>
				<div class="flex items-end gap-3 relative z-10">
					<span class="text-4xl font-bold font-mono text-white">164.5</span>
					<span class="text-emerald-glow text-xs font-bold mb-1"
						>+12h vs last month</span
					>
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
								stroke-dasharray="175"
								stroke-dashoffset="40"
								stroke-width="4"
							></circle>
						</svg>
						<span class="absolute text-[10px] font-bold">78%</span>
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
					<span class="text-4xl font-bold font-mono text-white">98%</span>
					<span class="text-gold-accent text-xs font-bold mb-1">Excellent Rating</span>
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
								stroke-dasharray="175"
								stroke-dashoffset="5"
								stroke-width="4"
							></circle>
						</svg>
						<span class="absolute text-[10px] font-bold">98%</span>
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
					<span class="text-4xl font-bold font-mono text-white">8h 12m</span>
					<div class="mt-3 h-1 w-full bg-white/10 rounded-full overflow-hidden">
						<div
							class="h-full bg-blue-500 w-[85%] shadow-[0_0_10px_rgba(59,130,246,0.5)]"
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
						<h2 class="text-2xl font-bold text-white">June 2024</h2>
						<p class="text-sm text-white/40">Monthly Attendance Performance</p>
					</div>
					<div class="flex gap-2">
						<button
							class="p-2 rounded-lg hover:bg-white/5 text-white/60 hover:text-white transition-colors"
						>
							<span class="material-symbols-outlined">chevron_left</span>
						</button>
						<button
							class="p-2 rounded-lg hover:bg-white/5 text-white/60 hover:text-white transition-colors"
						>
							<span class="material-symbols-outlined">chevron_right</span>
						</button>
					</div>
				</div>

				<!-- Calendar Grid Mockup -->
				<div class="grid grid-cols-7 gap-y-8 gap-x-4 text-center">
					<div class="text-[10px] font-bold uppercase text-white/30 mb-2">Mon</div>
					<div class="text-[10px] font-bold uppercase text-white/30 mb-2">Tue</div>
					<div class="text-[10px] font-bold uppercase text-white/30 mb-2">Wed</div>
					<div class="text-[10px] font-bold uppercase text-white/30 mb-2">Thu</div>
					<div class="text-[10px] font-bold uppercase text-white/30 mb-2">Fri</div>
					<div class="text-[10px] font-bold uppercase text-white/30 mb-2">Sat</div>
					<div class="text-[10px] font-bold uppercase text-white/30 mb-2">Sun</div>

					<!-- Days -->
					<button
						v-for="day in days"
						:key="day.date"
						class="aspect-square rounded-full flex flex-col items-center justify-center relative transition-all group"
						:class="[
							day.status === 'present' ? 'hover:bg-white/5' : '',
							day.isToday
								? 'border border-primary text-primary shadow-[0_0_10px_rgba(244,192,37,0.2)]'
								: 'text-white/60',
						]"
					>
						<span class="text-sm font-medium">{{ day.date }}</span>
						<span
							v-if="day.status === 'present'"
							class="w-1 h-1 rounded-full bg-emerald-glow mt-1"
						></span>
						<span
							v-if="day.status === 'absent'"
							class="w-1 h-1 rounded-full bg-red-400 mt-1"
						></span>
					</button>
				</div>
			</div>

			<!-- Recent Activity / Timeline -->
			<div class="col-span-1 space-y-6">
				<div class="flex items-center justify-between">
					<h3 class="font-bold text-lg text-white">Recent Activity</h3>
					<span class="text-[10px] font-bold text-primary uppercase cursor-pointer"
						>Filter</span
					>
				</div>

				<div class="space-y-4">
					<div
						class="glass-card p-4 rounded-xl border border-white/5 flex gap-4 items-center group hover:bg-white/5 transition-colors"
					>
						<div
							class="w-10 h-10 rounded-full bg-emerald-glow/10 border border-emerald-glow/20 flex items-center justify-center text-emerald-glow"
						>
							<span class="material-symbols-outlined text-lg">login</span>
						</div>
						<div class="flex-1">
							<div class="flex justify-between items-center mb-1">
								<p class="text-sm font-bold text-white">Shift Started</p>
								<span
									class="text-[10px] bg-emerald-glow/20 text-emerald-glow px-1.5 py-0.5 rounded font-bold uppercase"
									>On Time</span
								>
							</div>
							<p class="text-xs text-white/40">Today, 09:00 AM</p>
						</div>
					</div>

					<div
						class="glass-card p-4 rounded-xl border border-white/5 flex gap-4 items-center group hover:bg-white/5 transition-colors"
					>
						<div
							class="w-10 h-10 rounded-full bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400"
						>
							<span class="material-symbols-outlined text-lg">coffee</span>
						</div>
						<div class="flex-1">
							<div class="flex justify-between items-center mb-1">
								<p class="text-sm font-bold text-white">Break Ended</p>
								<span class="text-[10px] text-white/30">30m duration</span>
							</div>
							<p class="text-xs text-white/40">Jun 23, 01:30 PM</p>
						</div>
					</div>

					<div
						class="glass-card p-4 rounded-xl border border-white/5 flex gap-4 items-center group hover:bg-white/5 transition-colors"
					>
						<div
							class="w-10 h-10 rounded-full bg-red-500/10 border border-red-500/20 flex items-center justify-center text-red-400"
						>
							<span class="material-symbols-outlined text-lg">logout</span>
						</div>
						<div class="flex-1">
							<div class="flex justify-between items-center mb-1">
								<p class="text-sm font-bold text-white">Shift Ended</p>
								<span
									class="text-[10px] bg-white/10 text-white/50 px-1.5 py-0.5 rounded font-bold uppercase"
									>Verified</span
								>
							</div>
							<p class="text-xs text-white/40">Jun 23, 06:15 PM</p>
						</div>
					</div>
				</div>

				<button
					class="w-full py-4 text-xs font-bold uppercase tracking-widest text-white/40 hover:text-white glass-card rounded-xl hover:bg-white/5 transition-colors"
				>
					Load Previous History
				</button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";

const days = Array.from({ length: 30 }, (_, i) => ({
	date: i + 1,
	status: Math.random() > 0.8 ? "absent" : "present",
	isToday: i + 1 === 24,
}));
</script>
