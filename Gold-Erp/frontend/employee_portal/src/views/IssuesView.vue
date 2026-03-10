<template>
	<div class="flex flex-col gap-8">
		<div class="flex items-center justify-between">
			<div>
				<h2 class="text-3xl font-bold font-display text-white mb-2">Issues & Support</h2>
				<p class="text-white/40">Report attendance issues or get help from HR</p>
			</div>
			<button
				@click="showIssueModal = true"
				class="bg-primary text-background-dark px-6 py-3 rounded-xl font-bold flex items-center gap-2 hover:bg-yellow-400 transition-colors shadow-lg shadow-primary/20"
			>
				<span class="material-symbols-outlined">report</span>
				Report Issue
			</button>
		</div>

		<!-- Stats Cards -->
		<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
			<div class="glass-card p-6 rounded-2xl">
				<div class="flex items-center gap-3 mb-4">
					<div
						class="w-10 h-10 rounded-full bg-blue-400/10 flex items-center justify-center"
					>
						<span class="material-symbols-outlined text-blue-400">inbox</span>
					</div>
					<span class="text-xs font-bold uppercase text-white/60 tracking-wider"
						>Total Tickets</span
					>
				</div>
				<span class="text-4xl font-bold font-mono text-white">{{
					issuesStore.ticketStats.total
				}}</span>
			</div>

			<div class="glass-card p-6 rounded-2xl">
				<div class="flex items-center gap-3 mb-4">
					<div
						class="w-10 h-10 rounded-full bg-amber-400/10 flex items-center justify-center"
					>
						<span class="material-symbols-outlined text-amber-400">pending</span>
					</div>
					<span class="text-xs font-bold uppercase text-white/60 tracking-wider"
						>Open</span
					>
				</div>
				<span class="text-4xl font-bold font-mono text-white">{{
					issuesStore.ticketStats.open
				}}</span>
			</div>

			<div class="glass-card p-6 rounded-2xl">
				<div class="flex items-center gap-3 mb-4">
					<div
						class="w-10 h-10 rounded-full bg-emerald-glow/10 flex items-center justify-center"
					>
						<span class="material-symbols-outlined text-emerald-glow"
							>check_circle</span
						>
					</div>
					<span class="text-xs font-bold uppercase text-white/60 tracking-wider"
						>Resolved</span
					>
				</div>
				<span class="text-4xl font-bold font-mono text-white">{{
					issuesStore.ticketStats.closed
				}}</span>
			</div>
		</div>

		<!-- Tickets Table -->
		<div class="glass-card rounded-2xl border border-white/5 overflow-hidden">
			<div class="p-6 border-b border-white/5 flex items-center justify-between">
				<h3 class="font-bold text-lg text-white">My Tickets</h3>
				<div class="flex gap-2">
					<button
						@click="filterTickets = 'all'"
						class="px-4 py-2 rounded-lg text-xs font-bold uppercase transition"
						:class="
							filterTickets === 'all'
								? 'bg-white/10 text-white'
								: 'text-white/40 hover:text-white hover:bg-white/5'
						"
					>
						All
					</button>
					<button
						@click="filterTickets = 'open'"
						class="px-4 py-2 rounded-lg text-xs font-bold uppercase transition"
						:class="
							filterTickets === 'open'
								? 'bg-white/10 text-white'
								: 'text-white/40 hover:text-white hover:bg-white/5'
						"
					>
						Open
					</button>
					<button
						@click="filterTickets = 'resolved'"
						class="px-4 py-2 rounded-lg text-xs font-bold uppercase transition"
						:class="
							filterTickets === 'resolved'
								? 'bg-white/10 text-white'
								: 'text-white/40 hover:text-white hover:bg-white/5'
						"
					>
						Resolved
					</button>
				</div>
			</div>

			<div v-if="issuesStore.loading" class="p-8 text-center">
				<p class="text-white/40">Loading tickets...</p>
			</div>

			<div v-else-if="filteredTickets.length === 0" class="p-8 text-center">
				<div
					class="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-4"
				>
					<span class="material-symbols-outlined text-3xl text-white/20"
						>support_agent</span
					>
				</div>
				<h3 class="text-lg font-bold text-white mb-2">No Tickets Found</h3>
				<p class="text-white/40 text-sm">
					{{
						filterTickets === "all"
							? "You haven't created any tickets yet."
							: `No ${filterTickets} tickets.`
					}}
				</p>
			</div>

			<div v-else class="overflow-x-auto">
				<table class="w-full text-left">
					<thead
						class="bg-white/5 text-xs text-white/40 uppercase font-bold tracking-wider"
					>
						<tr>
							<th class="px-6 py-4">Subject</th>
							<th class="px-6 py-4">Type</th>
							<th class="px-6 py-4">Priority</th>
							<th class="px-6 py-4">Created</th>
							<th class="px-6 py-4 text-right">Status</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-white/5">
						<tr
							v-for="ticket in filteredTickets"
							:key="ticket.name"
							class="group hover:bg-white/5 transition-colors cursor-pointer"
							@click="viewTicket(ticket)"
						>
							<td class="px-6 py-4">
								<div class="flex items-center gap-3">
									<span
										class="w-2 h-2 rounded-full"
										:class="getStatusDotColor(ticket.status)"
									></span>
									<span class="font-bold text-white">{{ ticket.subject }}</span>
								</div>
							</td>
							<td class="px-6 py-4">
								<span class="text-white/60 text-sm">{{
									ticket.ticket_type || "General"
								}}</span>
							</td>
							<td class="px-6 py-4">
								<span
									class="text-[10px] font-bold px-2 py-1 rounded-md uppercase"
									:class="getPriorityClass(ticket.priority)"
								>
									{{ ticket.priority }}
								</span>
							</td>
							<td class="px-6 py-4">
								<span class="text-white/40 text-sm">{{
									formatDate(ticket.creation)
								}}</span>
							</td>
							<td class="px-6 py-4 text-right">
								<span
									class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold uppercase"
									:class="getStatusStyle(ticket.status)"
								>
									{{ ticket.status }}
								</span>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>

		<!-- Report Issue Modal -->
		<Teleport to="body">
			<div
				v-if="showIssueModal"
				class="fixed inset-0 z-50 flex items-center justify-center p-4"
				@click.self="showIssueModal = false"
			>
				<div class="absolute inset-0 bg-black/60"></div>
				<div
					class="relative bg-[#111420] rounded-2xl p-6 w-full max-w-md border border-white/10"
				>
					<h3 class="font-bold text-white text-lg mb-4">Report an Issue</h3>

					<div class="space-y-4">
						<div>
							<label class="block text-xs font-bold text-white/60 uppercase mb-2"
								>Subject</label
							>
							<input
								v-model="newIssue.subject"
								type="text"
								placeholder="Brief description of the issue..."
								class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-primary/50"
							/>
						</div>

						<div>
							<label class="block text-xs font-bold text-white/60 uppercase mb-2"
								>Issue Type</label
							>
							<select
								v-model="newIssue.issue_type"
								class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-primary/50"
							>
								<option value="" disabled>Select issue type...</option>
								<option
									v-for="type in issuesStore.issueTypes"
									:key="type.name"
									:value="type.name"
								>
									{{ type.name }}
								</option>
								<option value="Attendance">Attendance Issue</option>
								<option value="Payroll">Payroll Issue</option>
								<option value="Leave">Leave Issue</option>
								<option value="Manager">Manager Issue</option>
								<option value="Other">Other</option>
							</select>
						</div>

						<div>
							<label class="block text-xs font-bold text-white/60 uppercase mb-2"
								>Priority</label
							>
							<select
								v-model="newIssue.priority"
								class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-primary/50"
							>
								<option value="Low">Low</option>
								<option value="Medium">Medium</option>
								<option value="High">High</option>
								<option value="Urgent">Urgent</option>
							</select>
						</div>

						<div>
							<label class="block text-xs font-bold text-white/60 uppercase mb-2"
								>Description</label
							>
							<textarea
								v-model="newIssue.description"
								rows="4"
								placeholder="Provide details about the issue..."
								class="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-primary/50 resize-none"
							></textarea>
						</div>
					</div>

					<div class="flex gap-3 mt-6">
						<button
							@click="showIssueModal = false"
							class="flex-1 py-3 bg-white/5 hover:bg-white/10 rounded-xl text-white/60 text-sm font-bold transition-colors"
						>
							Cancel
						</button>
						<button
							@click="submitIssue"
							:disabled="!canSubmitIssue"
							class="flex-1 py-3 bg-primary text-black rounded-xl text-sm font-bold hover:bg-yellow-400 transition-colors disabled:opacity-50"
						>
							Submit Issue
						</button>
					</div>
				</div>
			</div>
		</Teleport>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useIssuesStore } from "@/stores/issues";

const issuesStore = useIssuesStore();

const showIssueModal = ref(false);
const filterTickets = ref("all");

const newIssue = ref({
	subject: "",
	description: "",
	issue_type: "",
	priority: "Medium",
});

// Filtered tickets
const filteredTickets = computed(() => {
	if (filterTickets.value === "open") {
		return issuesStore.openTickets;
	} else if (filterTickets.value === "resolved") {
		return issuesStore.resolvedTickets;
	}
	return issuesStore.tickets;
});

const canSubmitIssue = computed(() => {
	return newIssue.value.subject && newIssue.value.description;
});

// Actions
async function submitIssue() {
	if (!canSubmitIssue.value) return;

	await issuesStore.createIssue(
		newIssue.value.subject,
		newIssue.value.description,
		newIssue.value.issue_type || "Other",
		newIssue.value.priority
	);

	// Reset form
	showIssueModal.value = false;
	newIssue.value = {
		subject: "",
		description: "",
		issue_type: "",
		priority: "Medium",
	};
}

function viewTicket(ticket) {
	// Open ticket in desk or show details
	if (ticket.url) {
		window.open(ticket.url, "_blank");
	} else {
		window.open(`/app/hd-ticket/${ticket.name}`, "_blank");
	}
}

// Helpers
function getStatusDotColor(status) {
	switch (status) {
		case "Resolved":
		case "Closed":
			return "bg-emerald-glow";
		case "Open":
		case "Replied":
			return "bg-blue-400";
		default:
			return "bg-white/40";
	}
}

function getStatusStyle(status) {
	switch (status) {
		case "Resolved":
		case "Closed":
			return "bg-emerald-glow/20 text-emerald-glow";
		case "Open":
		case "Replied":
			return "bg-blue-400/20 text-blue-400";
		default:
			return "bg-white/10 text-white/40";
	}
}

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

function formatDate(dateStr) {
	if (!dateStr) return "";
	const date = new Date(dateStr);
	return date.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

onMounted(() => {
	issuesStore.init();
});
</script>
