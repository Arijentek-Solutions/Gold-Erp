import { defineStore } from "pinia";
import { createResource } from "frappe-ui";
import { ref, computed } from "vue";

export const useIssuesStore = defineStore("issues", () => {
	const tickets = ref([]);
	const ticketStats = ref({ total: 0, open: 0, closed: 0, pending: 0 });
	const issueTypes = ref([]);
	const loading = ref(false);

	// Get employee tickets
	const ticketsResource = createResource({
		url: "zevar_core.api.helpdesk.get_employee_tickets",
		auto: false,
		onSuccess(data) {
			tickets.value = data || [];
		},
	});

	// Get ticket stats
	const ticketStatsResource = createResource({
		url: "zevar_core.api.helpdesk.get_ticket_stats",
		auto: false,
		onSuccess(data) {
			if (data) {
				ticketStats.value = data;
			}
		},
	});

	// Get issue types
	const issueTypesResource = createResource({
		url: "zevar_core.api.helpdesk.get_issue_types",
		auto: false,
		onSuccess(data) {
			issueTypes.value = data || [];
		},
	});

	// Create issue
	const createIssueResource = createResource({
		url: "zevar_core.api.helpdesk.create_attendance_issue",
		auto: false,
	});

	// Computed
	const openTickets = computed(() => {
		return tickets.value.filter(
			(t) => t.status === "Open" || t.status === "Replied"
		);
	});

	const resolvedTickets = computed(() => {
		return tickets.value.filter(
			(t) => t.status === "Resolved" || t.status === "Closed"
		);
	});

	// Actions
	async function fetchTickets() {
		await ticketsResource.fetch();
	}

	async function fetchTicketStats() {
		await ticketStatsResource.fetch();
	}

	async function fetchIssueTypes() {
		await issueTypesResource.fetch();
	}

	async function createIssue(subject, description, issueType = "Other", priority = "Medium") {
		loading.value = true;
		try {
			const result = await createIssueResource.fetch({
				subject,
				description,
				issue_type: issueType,
				priority,
			});
			await fetchTickets();
			await fetchTicketStats();
			return result;
		} finally {
			loading.value = false;
		}
	}

	function init() {
		fetchTickets();
		fetchTicketStats();
		fetchIssueTypes();
	}

	return {
		tickets,
		ticketStats,
		issueTypes,
		loading,
		openTickets,
		resolvedTickets,
		fetchTickets,
		fetchTicketStats,
		fetchIssueTypes,
		createIssue,
		init,
	};
});
