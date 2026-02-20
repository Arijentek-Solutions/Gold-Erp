<template>
	<div class="h-full flex flex-col gap-6 p-10">
		<div class="flex items-center justify-between shrink-0">
			<div>
				<h2 class="text-3xl font-bold font-display text-white mb-1">My Tasks</h2>
				<p class="text-white/50 text-sm">
					Track and manage your daily jewelry collection goals
				</p>
			</div>
		</div>

		<!-- Quick Add Task -->
		<div class="shrink-0">
			<div class="glass-card p-4 rounded-xl flex items-center gap-4">
				<div
					class="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-primary"
				>
					<span class="material-symbols-outlined">add_task</span>
				</div>
				<input
					type="text"
					placeholder="Add a new task to your board..."
					class="flex-1 bg-transparent border-none outline-none text-white placeholder:text-white/20 text-sm"
				/>
				<button
					class="bg-primary hover:bg-yellow-400 text-black px-6 py-2 rounded-lg text-xs font-bold tracking-wide transition-all uppercase"
				>
					Add Task
				</button>
			</div>
		</div>

		<!-- Task Columns -->
		<div class="flex-1 overflow-y-auto custom-scrollbar">
			<div class="grid grid-cols-1 md:grid-cols-3 gap-6 pb-4 h-full">
				<div v-for="col in columns" :key="col.title" class="flex flex-col h-full">
					<div
						class="flex items-center gap-3 mb-4 p-2 bg-white/5 rounded-lg border border-white/5 shrink-0"
					>
						<div class="size-2.5 rounded-full" :class="col.dotClass"></div>
						<h3 class="text-xs font-black uppercase tracking-widest text-white/70">
							{{ col.title }}
						</h3>
						<span
							class="ml-auto text-[10px] px-2 py-0.5 rounded-full bg-white/10 text-white/50 font-mono"
							>{{ col.tasks.length }}</span
						>
					</div>

					<div class="space-y-3 flex-1 overflow-y-auto custom-scrollbar pr-2">
						<div
							v-for="task in col.tasks"
							:key="task.title"
							class="glass-card glass-card-hover rounded-xl p-5 transition-all duration-300 hover:-translate-y-1 cursor-pointer group border border-white/5 hover:border-white/10"
						>
							<div class="flex items-start justify-between mb-3">
								<span
									class="text-[10px] font-bold px-2 py-1 rounded-md uppercase tracking-wide"
									:class="task.tagClass"
									>{{ task.tag }}</span
								>
								<span class="text-[10px] text-white/30">{{ task.date }}</span>
							</div>
							<h4
								class="font-bold text-sm mb-2 text-white group-hover:text-primary transition-colors leading-snug"
							>
								{{ task.title }}
							</h4>
							<p class="text-xs text-white/40 leading-relaxed mb-4">
								{{ task.desc }}
							</p>
							<div class="flex items-center gap-2">
								<div
									class="size-6 rounded-full bg-white/5 border border-white/10 flex items-center justify-center ring-1 ring-white/5"
								>
									<span class="text-[9px] font-bold text-white/70">{{
										task.assignee
									}}</span>
								</div>
								<div class="flex-1 h-1 bg-white/5 rounded-full overflow-hidden">
									<div
										class="h-full rounded-full transition-all duration-1000"
										:class="task.progressClass"
										:style="{ width: task.progress + '%' }"
									></div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";

const columns = [
	{
		title: "Assigned",
		dotClass: "bg-amber-400",
		tasks: [
			{
				title: "Inventory Stock Count",
				desc: "Complete the weekly stock count for Gold category items",
				tag: "Urgent",
				tagClass: "bg-red-500/15 text-red-400",
				date: "Today",
				assignee: "A",
				progress: 20,
				progressClass: "bg-amber-400",
			},
			{
				title: "Customer Follow-up",
				desc: "Contact VIP customers for new collection preview",
				tag: "Medium",
				tagClass: "bg-amber-500/15 text-amber-400",
				date: "Tomorrow",
				assignee: "R",
				progress: 0,
				progressClass: "bg-amber-400",
			},
		],
	},
	{
		title: "In Progress",
		dotClass: "bg-portal-primary",
		tasks: [
			{
				title: "Display Arrangement",
				desc: "Reorganize the showcase display for the new diamond collection",
				tag: "High",
				tagClass: "bg-portal-primary/15 text-portal-primary",
				date: "In Progress",
				assignee: "S",
				progress: 65,
				progressClass: "bg-portal-primary",
			},
			{
				title: "Price Tag Update",
				desc: "Update price tags for items affected by the latest gold rate change",
				tag: "Medium",
				tagClass: "bg-amber-500/15 text-amber-400",
				date: "In Progress",
				assignee: "M",
				progress: 40,
				progressClass: "bg-portal-primary",
			},
		],
	},
	{
		title: "Completed",
		dotClass: "bg-portal-accent-teal",
		tasks: [
			{
				title: "Monthly Report",
				desc: "Submitted the monthly sales performance report",
				tag: "Done",
				tagClass: "bg-green-500/15 text-green-400",
				date: "Yesterday",
				assignee: "A",
				progress: 100,
				progressClass: "bg-portal-accent-teal",
			},
			{
				title: "Staff Training",
				desc: "Completed the gemstone identification training module",
				tag: "Done",
				tagClass: "bg-green-500/15 text-green-400",
				date: "2 days ago",
				assignee: "R",
				progress: 100,
				progressClass: "bg-portal-accent-teal",
			},
		],
	},
];
</script>
