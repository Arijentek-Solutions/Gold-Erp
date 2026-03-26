<template>
	<div class="h-full flex flex-col gap-6">
		<div class="flex items-center justify-between shrink-0">
			<div>
				<h2 class="premium-title">My Tasks</h2>
				<p class="premium-subtitle !text-sm">
					Track and manage your daily jewelry collection goals
				</p>
			</div>
		</div>

		<!-- Quick Add Task -->
		<div class="shrink-0">
			<div class="premium-card !p-4 flex items-center gap-4">
				<div
					class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary border border-primary/20"
				>
					<span class="material-symbols-outlined">add_task</span>
				</div>
				<input
					v-model="newTodoText"
					type="text"
					placeholder="Add a new task to your board..."
					class="flex-1 bg-transparent border-none outline-none text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-white/20 text-sm"
					@keyup.enter="addTodo"
				/>
				<select
					v-model="newTodoPriority"
					class="bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-xl px-3 h-10 text-xs text-gray-700 dark:text-white/70 outline-none cursor-pointer premium-select m-0"
				>
					<option
						value="Low"
						class="bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
					>
						Low
					</option>
					<option
						value="Medium"
						class="bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
					>
						Medium
					</option>
					<option
						value="High"
						class="bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
					>
						High
					</option>
				</select>
				<button
					@click="addTodo"
					:disabled="!newTodoText.trim() || tasksStore.loading"
					class="btn-vibrant-sky h-10 px-6 rounded-xl text-xs font-black transition-all flex items-center justify-center gap-2 m-0"
				>
					<span class="material-symbols-outlined text-sm">add</span>
					Add Task
				</button>
			</div>
		</div>

		<!-- Task Columns -->
		<div class="flex-1 overflow-y-auto custom-scrollbar">
			<div class="grid grid-cols-1 md:grid-cols-3 gap-6 pb-4 h-full">
				<!-- Assigned/Pending Tasks -->
				<div
					class="flex flex-col h-full"
					@dragover.prevent="onDragOver($event, 'assigned')"
					@dragleave="onDragLeave($event)"
					@drop="onDrop($event, 'assigned')"
				>
					<div
						class="flex items-center gap-3 mb-4 p-2 bg-white/5 rounded-lg border border-white/5 shrink-0"
					>
						<div class="size-2.5 rounded-full bg-amber-400"></div>
						<h3 class="text-xs font-black tracking-widest text-white/70">Assigned</h3>
						<span
							class="ml-auto text-[10px] px-2 py-0.5 rounded-full bg-white/10 text-white/50 font-mono"
							>{{ assignedTasks.length }}</span
						>
					</div>

					<div
						class="space-y-3 flex-1 overflow-y-auto custom-scrollbar pr-2 drop-zone"
						:class="{ 'drop-zone-active': dropZone === 'assigned' }"
					>
						<div
							v-if="!tasksStore.gameplanInstalled"
							class="premium-card !p-5 text-center"
						>
							<span
								class="material-symbols-outlined text-3xl text-gray-400 dark:text-white/20 mb-2"
								>extension</span
							>
							<p class="premium-subtitle !text-sm">Gameplan not installed</p>
							<p class="premium-subtitle !text-xs mt-1">
								Install Gameplan app to see tasks
							</p>
						</div>

						<div
							v-else-if="assignedTasks.length === 0"
							class="premium-card !p-5 text-center"
						>
							<span
								class="material-symbols-outlined text-3xl text-gray-400 dark:text-white/20 mb-2"
								>check_circle</span
							>
							<p class="premium-subtitle !text-sm">No assigned tasks</p>
							<p class="premium-subtitle !text-xs mt-1 text-white/30">
								Drop tasks here
							</p>
						</div>

						<div
							v-for="task in assignedTasks"
							:key="task.id"
							:draggable="true"
							@dragstart="onDragStart($event, task, 'task')"
							@dragend="onDragEnd"
							class="premium-card !p-5 transition-all duration-300 hover:-translate-y-1 cursor-pointer group border border-gray-100 dark:border-white/5 hover:border-primary/20"
							:class="{ 'opacity-50': draggedItem?.id === task.id }"
							@click="openTask(task)"
						>
							<div class="flex items-start justify-between mb-3">
								<span
									class="text-[10px] font-bold px-2 py-1 rounded-md tracking-wide"
									:class="getPriorityClass(task.priority)"
									>{{ task.priority }}</span
								>
								<span class="text-[10px] text-gray-500 dark:text-white/30">{{
									formatDueDate(task.due_date)
								}}</span>
							</div>
							<h4
								class="font-bold text-sm mb-2 text-gray-900 dark:text-white group-hover:text-primary transition-colors leading-snug"
							>
								{{ task.title }}
							</h4>
							<p
								v-if="task.description"
								class="text-xs text-gray-500 dark:text-white/40 leading-relaxed mb-4"
							>
								{{ truncateText(task.description, 80) }}
							</p>
							<div class="flex items-center gap-2">
								<div
									class="size-6 rounded-lg bg-gray-100 dark:bg-white/5 border border-gray-200 dark:border-white/10 flex items-center justify-center"
								>
									<span
										class="text-[9px] font-bold text-gray-500 dark:text-white/70"
										>GP</span
									>
								</div>
								<div class="flex-1">
									<span class="text-[10px] text-gray-500 dark:text-white/40">{{
										task.project_name || "No Project"
									}}</span>
								</div>
								<span
									v-if="task.is_overdue"
									class="text-[10px] px-2 py-0.5 rounded-full bg-red-500/20 text-red-500 font-bold"
									>Overdue</span
								>
							</div>
						</div>
					</div>
				</div>

				<!-- In Progress Tasks -->
				<div
					class="flex flex-col h-full"
					@dragover.prevent="onDragOver($event, 'inProgress')"
					@dragleave="onDragLeave($event)"
					@drop="onDrop($event, 'inProgress')"
				>
					<div
						class="flex items-center gap-3 mb-4 p-2 bg-white/5 rounded-lg border border-white/5 shrink-0"
					>
						<div class="size-2.5 rounded-full bg-portal-primary"></div>
						<h3 class="text-xs font-black tracking-widest text-white/70">
							In Progress
						</h3>
						<span
							class="ml-auto text-[10px] px-2 py-0.5 rounded-full bg-white/10 text-white/50 font-mono"
							>{{ inProgressTasks.length }}</span
						>
					</div>

					<div
						class="space-y-3 flex-1 overflow-y-auto custom-scrollbar pr-2 drop-zone"
						:class="{ 'drop-zone-active': dropZone === 'inProgress' }"
					>
						<div
							v-if="inProgressTasks.length === 0"
							class="premium-card !p-5 text-center"
						>
							<span
								class="material-symbols-outlined text-3xl text-gray-400 dark:text-white/20 mb-2"
								>hourglass_empty</span
							>
							<p class="premium-subtitle !text-sm">No tasks in progress</p>
						</div>

						<div
							v-for="task in inProgressTasks"
							:key="task.id"
							:draggable="true"
							@dragstart="onDragStart($event, task, 'task')"
							@dragend="onDragEnd"
							class="premium-card !p-5 transition-all duration-300 hover:-translate-y-1 cursor-pointer group border border-gray-100 dark:border-white/5 hover:border-primary/20"
							:class="{ 'opacity-50': draggedItem?.id === task.id }"
							@click="openTask(task)"
						>
							<div class="flex items-start justify-between mb-3">
								<span
									class="text-[10px] font-bold px-2 py-1 rounded-md tracking-wide"
									:class="getPriorityClass(task.priority)"
									>{{ task.priority }}</span
								>
								<span class="text-[10px] text-gray-500 dark:text-white/30">{{
									formatDueDate(task.due_date)
								}}</span>
							</div>
							<h4
								class="font-bold text-sm mb-2 text-gray-900 dark:text-white group-hover:text-primary transition-colors leading-snug"
							>
								{{ task.title }}
							</h4>
							<p
								v-if="task.description"
								class="text-xs text-gray-500 dark:text-white/40 leading-relaxed mb-4"
							>
								{{ truncateText(task.description, 80) }}
							</p>
							<div class="flex items-center gap-2">
								<div
									class="size-6 rounded-lg bg-gray-100 dark:bg-white/5 border border-gray-200 dark:border-white/10 flex items-center justify-center"
								>
									<span
										class="text-[9px] font-bold text-gray-500 dark:text-white/70"
										>GP</span
									>
								</div>
								<div class="flex-1">
									<span class="text-[10px] text-gray-500 dark:text-white/40">{{
										task.project_name || "No Project"
									}}</span>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Personal TODOs -->
				<div
					class="flex flex-col h-full"
					@dragover.prevent="onDragOver($event, 'myTasks')"
					@dragleave="onDragLeave($event)"
					@drop="onDrop($event, 'myTasks')"
				>
					<div
						class="flex items-center gap-3 mb-4 p-2 bg-white/5 rounded-lg border border-white/5 shrink-0"
					>
						<div class="size-2.5 rounded-full bg-portal-accent-teal"></div>
						<h3 class="text-xs font-black tracking-widest text-white/70">My Tasks</h3>
						<span
							class="ml-auto text-[10px] px-2 py-0.5 rounded-full bg-white/10 text-white/50 font-mono"
							>{{ tasksStore.openTodos.length }}</span
						>
					</div>

					<div
						class="space-y-3 flex-1 overflow-y-auto custom-scrollbar pr-2 drop-zone"
						:class="{ 'drop-zone-active': dropZone === 'myTasks' }"
					>
						<div
							v-if="sortedOpenTodos.length === 0"
							class="premium-card !p-5 text-center"
						>
							<span
								class="material-symbols-outlined text-3xl text-gray-400 dark:text-white/20 mb-2"
								>task_alt</span
							>
							<p class="premium-subtitle !text-sm">No personal tasks</p>
							<p class="premium-subtitle !text-xs mt-1">
								Add a task above to get started
							</p>
						</div>

						<div
							v-for="todo in sortedOpenTodos"
							:key="todo.id"
							:draggable="true"
							@dragstart="onDragStart($event, todo, 'todo')"
							@dragend="onDragEnd"
							class="premium-card !p-5 transition-all duration-300 hover:-translate-y-1 cursor-pointer group border border-gray-100 dark:border-white/5 hover:border-primary/20"
							:class="{ 'opacity-50': draggedItem?.id === todo.id }"
						>
							<div class="flex items-start justify-between mb-3">
								<span
									class="text-[10px] font-bold px-2 py-1 rounded-md tracking-wide"
									:class="getPriorityClass(todo.priority)"
									>{{ todo.priority }}</span
								>
								<button
									@click.stop="deleteTodo(todo.id)"
									class="text-gray-400 dark:text-white/30 hover:text-red-500 transition-colors"
								>
									<span class="material-symbols-outlined text-lg">delete</span>
								</button>
							</div>
							<h4
								class="font-bold text-sm mb-2 text-gray-900 dark:text-white group-hover:text-primary transition-colors leading-snug"
							>
								{{ todo.description }}
							</h4>
							<div class="flex items-center gap-2">
								<div class="flex-1">
									<span class="text-[10px] text-gray-500 dark:text-white/40">{{
										formatDate(todo.date)
									}}</span>
								</div>
								<button
									@click.stop="toggleTodoStatus(todo)"
									class="text-emerald-600 dark:text-emerald-400 hover:text-emerald-500 transition-colors"
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
const newTodoPriority = ref("Medium");

// Drag and drop state
const draggedItem = ref(null);
const draggedType = ref(null);
const dropZone = ref(null);

// Computed task groups
const assignedTasks = computed(() => {
	return tasksStore.tasks.filter(
		(t) => t.status === "Backlog" || t.status === "Todo" || t.status === "Open"
	);
});

const inProgressTasks = computed(() => {
	return tasksStore.tasks.filter((t) => t.status === "In Progress");
});

// Priority order for sorting
const priorityOrder = { High: 1, Medium: 2, Low: 3 };

// Sort open todos by priority
const sortedOpenTodos = computed(() => {
	return [...tasksStore.openTodos].sort((a, b) => {
		return (priorityOrder[a.priority] || 99) - (priorityOrder[b.priority] || 99);
	});
});

// Actions
async function addTodo() {
	if (!newTodoText.value.trim()) return;

	await tasksStore.createTodo(newTodoText.value.trim(), null, newTodoPriority.value);
	newTodoText.value = "";
	newTodoPriority.value = "Medium";
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

// Drag and drop handlers
function onDragStart(event, item, type) {
	draggedItem.value = item;
	draggedType.value = type;
	event.dataTransfer.effectAllowed = "move";
	event.dataTransfer.setData("text/plain", item.id);
}

function onDragEnd() {
	draggedItem.value = null;
	draggedType.value = null;
	dropZone.value = null;
}

function onDragOver(event, zone) {
	event.preventDefault();
	dropZone.value = zone;
}

function onDragLeave(event) {
	// Only clear if we're leaving the column entirely
	if (!event.currentTarget.contains(event.relatedTarget)) {
		dropZone.value = null;
	}
}

async function onDrop(event, targetZone) {
	event.preventDefault();
	dropZone.value = null;

	if (!draggedItem.value) return;

	const item = draggedItem.value;
	const sourceType = draggedType.value;

	// Reset drag state
	draggedItem.value = null;
	draggedType.value = null;

	// Handle dropping Gameplan tasks
	if (sourceType === "task") {
		let newStatus = null;

		if (targetZone === "assigned") {
			newStatus = "Todo";
		} else if (targetZone === "inProgress") {
			newStatus = "In Progress";
		} else if (targetZone === "myTasks") {
			// Gameplan tasks can't become personal todos
			return;
		}

		if (newStatus && item.status !== newStatus) {
			await tasksStore.updateTaskStatus(item.id, newStatus);
		}
	}

	// Handle dropping personal todos
	if (sourceType === "todo") {
		// Personal todos stay in My Tasks column - just reorder within
		// For now, we don't support moving personal todos to other columns
		// as they are different document types
	}
}

onMounted(() => {
	tasksStore.init();
});
</script>

<style scoped>
.drop-zone {
	transition: all 0.2s ease;
	min-height: 100px;
	border-radius: 0.75rem;
}

.drop-zone-active {
	background: rgba(56, 189, 248, 0.1);
	border: 2px dashed rgba(56, 189, 248, 0.4);
}
</style>
