<template>
	<div class="h-full flex flex-col gap-6">
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
					v-model="newTodoText"
					type="text"
					placeholder="Add a new task to your board..."
					class="flex-1 bg-transparent border-none outline-none text-white placeholder:text-white/20 text-sm"
					@keyup.enter="addTodo"
				/>
				<button
					@click="addTodo"
					:disabled="!newTodoText.trim() || tasksStore.loading"
					class="bg-primary hover:bg-yellow-400 text-black px-6 py-2 rounded-lg text-xs font-bold tracking-wide transition-all uppercase disabled:opacity-50"
				>
					Add Task
				</button>
			</div>
		</div>

		<!-- Task Columns -->
		<div class="flex-1 overflow-y-auto custom-scrollbar">
			<div class="grid grid-cols-1 md:grid-cols-3 gap-6 pb-4 h-full">
				<!-- Assigned/Pending Tasks -->
				<div class="flex flex-col h-full">
					<div
						class="flex items-center gap-3 mb-4 p-2 bg-white/5 rounded-lg border border-white/5 shrink-0"
					>
						<div class="size-2.5 rounded-full bg-amber-400"></div>
						<h3 class="text-xs font-black uppercase tracking-widest text-white/70">
							Assigned
						</h3>
						<span
							class="ml-auto text-[10px] px-2 py-0.5 rounded-full bg-white/10 text-white/50 font-mono"
							>{{ assignedTasks.length }}</span
						>
					</div>

					<div class="space-y-3 flex-1 overflow-y-auto custom-scrollbar pr-2">
						<div
							v-if="!tasksStore.gameplanInstalled"
							class="glass-card rounded-xl p-5 text-center"
						>
							<span class="material-symbols-outlined text-3xl text-white/20 mb-2"
								>extension</span
							>
							<p class="text-white/40 text-sm">Gameplan not installed</p>
							<p class="text-white/30 text-xs mt-1">
								Install Gameplan app to see tasks
							</p>
						</div>

						<div
							v-else-if="assignedTasks.length === 0"
							class="glass-card rounded-xl p-5 text-center"
						>
							<span class="material-symbols-outlined text-3xl text-white/20 mb-2"
								>check_circle</span
							>
							<p class="text-white/40 text-sm">No assigned tasks</p>
						</div>

						<div
							v-for="task in assignedTasks"
							:key="task.id"
							class="glass-card glass-card-hover rounded-xl p-5 transition-all duration-300 hover:-translate-y-1 cursor-pointer group border border-white/5 hover:border-white/10"
							@click="openTask(task)"
						>
							<div class="flex items-start justify-between mb-3">
								<span
									class="text-[10px] font-bold px-2 py-1 rounded-md uppercase tracking-wide"
									:class="getPriorityClass(task.priority)"
									>{{ task.priority }}</span
								>
								<span class="text-[10px] text-white/30">{{
									formatDueDate(task.due_date)
								}}</span>
							</div>
							<h4
								class="font-bold text-sm mb-2 text-white group-hover:text-primary transition-colors leading-snug"
							>
								{{ task.title }}
							</h4>
							<p
								v-if="task.description"
								class="text-xs text-white/40 leading-relaxed mb-4"
							>
								{{ truncateText(task.description, 80) }}
							</p>
							<div class="flex items-center gap-2">
								<div
									class="size-6 rounded-full bg-white/5 border border-white/10 flex items-center justify-center ring-1 ring-white/5"
								>
									<span class="text-[9px] font-bold text-white/70">GP</span>
								</div>
								<div class="flex-1">
									<span class="text-xs text-white/40">{{
										task.project_name || "No Project"
									}}</span>
								</div>
								<span
									v-if="task.is_overdue"
									class="text-[10px] px-2 py-0.5 rounded-full bg-red-500/20 text-red-400"
									>Overdue</span
								>
							</div>
						</div>
					</div>
				</div>

				<!-- In Progress Tasks -->
				<div class="flex flex-col h-full">
					<div
						class="flex items-center gap-3 mb-4 p-2 bg-white/5 rounded-lg border border-white/5 shrink-0"
					>
						<div class="size-2.5 rounded-full bg-portal-primary"></div>
						<h3 class="text-xs font-black uppercase tracking-widest text-white/70">
							In Progress
						</h3>
						<span
							class="ml-auto text-[10px] px-2 py-0.5 rounded-full bg-white/10 text-white/50 font-mono"
							>{{ inProgressTasks.length }}</span
						>
					</div>

					<div class="space-y-3 flex-1 overflow-y-auto custom-scrollbar pr-2">
						<div
							v-if="inProgressTasks.length === 0"
							class="glass-card rounded-xl p-5 text-center"
						>
							<span class="material-symbols-outlined text-3xl text-white/20 mb-2"
								>hourglass_empty</span
							>
							<p class="text-white/40 text-sm">No tasks in progress</p>
						</div>

						<div
							v-for="task in inProgressTasks"
							:key="task.id"
							class="glass-card glass-card-hover rounded-xl p-5 transition-all duration-300 hover:-translate-y-1 cursor-pointer group border border-white/5 hover:border-white/10"
							@click="openTask(task)"
						>
							<div class="flex items-start justify-between mb-3">
								<span
									class="text-[10px] font-bold px-2 py-1 rounded-md uppercase tracking-wide"
									:class="getPriorityClass(task.priority)"
									>{{ task.priority }}</span
								>
								<span class="text-[10px] text-white/30">{{
									formatDueDate(task.due_date)
								}}</span>
							</div>
							<h4
								class="font-bold text-sm mb-2 text-white group-hover:text-primary transition-colors leading-snug"
							>
								{{ task.title }}
							</h4>
							<p
								v-if="task.description"
								class="text-xs text-white/40 leading-relaxed mb-4"
							>
								{{ truncateText(task.description, 80) }}
							</p>
							<div class="flex items-center gap-2">
								<div
									class="size-6 rounded-full bg-white/5 border border-white/10 flex items-center justify-center ring-1 ring-white/5"
								>
									<span class="text-[9px] font-bold text-white/70">GP</span>
								</div>
								<div class="flex-1">
									<span class="text-xs text-white/40">{{
										task.project_name || "No Project"
									}}</span>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Personal TODOs -->
				<div class="flex flex-col h-full">
					<div
						class="flex items-center gap-3 mb-4 p-2 bg-white/5 rounded-lg border border-white/5 shrink-0"
					>
						<div class="size-2.5 rounded-full bg-portal-accent-teal"></div>
						<h3 class="text-xs font-black uppercase tracking-widest text-white/70">
							My Tasks
						</h3>
						<span
							class="ml-auto text-[10px] px-2 py-0.5 rounded-full bg-white/10 text-white/50 font-mono"
							>{{ tasksStore.openTodos.length }}</span
						>
					</div>

					<div class="space-y-3 flex-1 overflow-y-auto custom-scrollbar pr-2">
						<div
							v-if="tasksStore.openTodos.length === 0"
							class="glass-card rounded-xl p-5 text-center"
						>
							<span class="material-symbols-outlined text-3xl text-white/20 mb-2"
								>task_alt</span
							>
							<p class="text-white/40 text-sm">No personal tasks</p>
							<p class="text-white/30 text-xs mt-1">
								Add a task above to get started
							</p>
						</div>

						<div
							v-for="todo in tasksStore.openTodos"
							:key="todo.id"
							class="glass-card glass-card-hover rounded-xl p-5 transition-all duration-300 hover:-translate-y-1 cursor-pointer group border border-white/5 hover:border-white/10"
						>
							<div class="flex items-start justify-between mb-3">
								<span
									class="text-[10px] font-bold px-2 py-1 rounded-md uppercase tracking-wide"
									:class="getPriorityClass(todo.priority)"
									>{{ todo.priority }}</span
								>
								<button
									@click.stop="deleteTodo(todo.id)"
									class="text-white/30 hover:text-red-400 transition-colors"
								>
									<span class="material-symbols-outlined text-lg">delete</span>
								</button>
							</div>
							<h4
								class="font-bold text-sm mb-2 text-white group-hover:text-primary transition-colors leading-snug"
								@click="toggleTodoStatus(todo)"
							>
								{{ todo.description }}
							</h4>
							<div class="flex items-center gap-2">
								<div class="flex-1">
									<span class="text-xs text-white/40">{{
										formatDate(todo.date)
									}}</span>
								</div>
								<button
									@click.stop="toggleTodoStatus(todo)"
									class="text-portal-accent-teal hover:text-emerald-glow transition-colors"
								>
									<span class="material-symbols-outlined text-lg"
										>check_circle</span
									>
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useTasksStore } from "@/stores/tasks";

const tasksStore = useTasksStore();
const newTodoText = ref("");

// Computed task groups
const assignedTasks = computed(() => {
	return tasksStore.tasks.filter(
		(t) => t.status === "Backlog" || t.status === "Todo" || t.status === "Open"
	);
});

const inProgressTasks = computed(() => {
	return tasksStore.tasks.filter((t) => t.status === "In Progress");
});

// Actions
async function addTodo() {
	if (!newTodoText.value.trim()) return;

	await tasksStore.createTodo(newTodoText.value.trim());
	newTodoText.value = "";
}

async function toggleTodoStatus(todo) {
	await tasksStore.toggleTodo(todo.id, todo.status);
}

async function deleteTodo(todoId) {
	await tasksStore.deleteTodoItem(todoId);
}

function openTask(task) {
	if (task.url) {
		window.open(task.url, "_blank");
	}
}

// Helpers
function getPriorityClass(priority) {
	switch (priority) {
		case "High":
		case "Urgent":
			return "bg-red-500/15 text-red-400";
		case "Medium":
			return "bg-amber-500/15 text-amber-400";
		case "Low":
			return "bg-blue-500/15 text-blue-400";
		default:
			return "bg-white/10 text-white/50";
	}
}

function formatDueDate(dateStr) {
	if (!dateStr) return "No due date";

	const date = new Date(dateStr);
	const today = new Date();
	const tomorrow = new Date(today);
	tomorrow.setDate(tomorrow.getDate() + 1);

	if (date.toDateString() === today.toDateString()) return "Today";
	if (date.toDateString() === tomorrow.toDateString()) return "Tomorrow";

	return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function formatDate(dateStr) {
	if (!dateStr) return "No date";
	const date = new Date(dateStr);
	return date.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

function truncateText(text, maxLength) {
	if (!text) return "";
	return text.length > maxLength ? text.substring(0, maxLength) + "..." : text;
}

onMounted(() => {
	tasksStore.init();
});
</script>
