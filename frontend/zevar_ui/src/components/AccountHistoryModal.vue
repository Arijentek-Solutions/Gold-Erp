<template>
	<div v-if="show" class="modal-overlay" @click.self="close">
		<div class="modal-content">
			<div class="modal-header">
				<h2>Recent Activity</h2>
				<button class="close-btn" @click="close">&times;</button>
			</div>

			<div class="modal-body">
				<!-- Today's Summary -->
				<div class="summary-card" v-if="summary">
					<div class="summary-row">
						<div class="summary-item">
							<span class="summary-value">{{ summary.transaction_count }}</span>
							<span class="summary-label">Transactions</span>
						</div>
						<div class="summary-item">
							<span class="summary-value">${{ formatAmount(summary.total_sales) }}</span>
							<span class="summary-label">Total Sales</span>
						</div>
						<div class="summary-item">
							<span class="summary-value">${{ formatAmount(summary.average_sale) }}</span>
							<span class="summary-label">Avg Sale</span>
						</div>
					</div>
				</div>

				<!-- Activity List -->
				<div class="activity-section">
					<h4>Recent Transactions</h4>
					<div class="activity-list" v-if="transactions.length">
						<div v-for="tx in transactions" :key="tx.name" class="activity-item" @click="viewTransaction(tx.name)">
							<div class="activity-icon" :class="tx.type">
								{{ tx.type === 'sale' ? '💰' : tx.type === 'return' ? '↩️' : '📋' }}
							</div>
							<div class="activity-content">
								<div class="activity-title">{{ tx.customer || 'Walk-In Customer' }}</div>
								<div class="activity-meta">
									<span>{{ tx.name }}</span>
									<span>{{ formatTime(tx.posting_time) }}</span>
								</div>
							</div>
							<div class="activity-amount" :class="{ positive: tx.type === 'sale', negative: tx.type === 'return' }">
								{{ tx.type === 'return' ? '-' : '' }}${{ formatAmount(tx.grand_total) }}
							</div>
						</div>
					</div>
					<div v-else class="empty-state">
						No recent transactions
					</div>
				</div>

				<!-- Session Info -->
				<div class="session-section" v-if="session">
					<h4>Current Session</h4>
					<div class="session-info">
						<div class="session-row">
							<span>Started</span>
							<span>{{ formatTime(session.opening_time) }}</span>
						</div>
						<div class="session-row">
							<span>Duration</span>
							<span>{{ session.duration_hours }}h</span>
						</div>
						<div class="session-row">
							<span>Opening Balance</span>
							<span>${{ formatAmount(session.opening_balance) }}</span>
						</div>
						<div class="session-row">
							<span>Sales Count</span>
							<span>{{ session.sales_count }}</span>
						</div>
					</div>
				</div>
			</div>

			<div class="modal-footer">
				<router-link to="/history" class="btn btn-secondary" @click="close">
					View Full History
				</router-link>
				<button class="btn btn-primary" @click="close">
					Close
				</button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { createResource } from 'frappe-ui'

const props = defineProps({
	show: { type: Boolean, default: false }
})

const emit = defineEmits(['close'])

const transactions = ref([])
const summary = ref(null)
const session = ref(null)

const historyResource = createResource({
	url: 'zevar_core.api.sales_history.get_sales_history',
	auto: false,
	onSuccess(data) {
		transactions.value = (data.sales || []).map(s => ({
			...s,
			type: s.status === 'Return' ? 'return' : 'sale'
		}))
	}
})

const summaryResource = createResource({
	url: 'zevar_core.api.sales_history.get_sales_summary',
	auto: false,
	onSuccess(data) {
		summary.value = data.summary
	}
})

const sessionResource = createResource({
	url: 'zevar_core.api.pos_session.get_session_status',
	auto: false,
	onSuccess(data) {
		if (data.has_active_session) {
			session.value = data.session
		}
	}
})

function formatAmount(amount) {
	if (!amount) return '0.00'
	return Number(amount).toFixed(2)
}

function formatTime(timeStr) {
	if (!timeStr) return ''
	const [hours, minutes] = timeStr.split(':')
	const h = parseInt(hours)
	const ampm = h >= 12 ? 'PM' : 'AM'
	const h12 = h % 12 || 12
	return `${h12}:${minutes} ${ampm}`
}

function viewTransaction(name) {
	window.open(`/app/sales-invoice/${name}`, '_blank')
}

function close() {
	emit('close')
}

async function loadData() {
	await Promise.all([
		historyResource.submit({ page: 1, page_size: 10 }),
		summaryResource.submit({}),
		sessionResource.submit({})
	])
}

watch(() => props.show, (val) => {
	if (val) loadData()
})

onMounted(() => {
	if (props.show) loadData()
})
</script>

<style scoped>
.modal-overlay {
	position: fixed;
	inset: 0;
	background: rgba(0, 0, 0, 0.7);
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 1000;
}

.modal-content {
	background: #1e293b;
	border-radius: 16px;
	width: 90%;
	max-width: 500px;
	max-height: 90vh;
	overflow-y: auto;
}

.modal-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 20px 24px;
	border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h2 {
	color: white;
	font-size: 18px;
	margin: 0;
}

.close-btn {
	background: transparent;
	border: none;
	color: rgba(255, 255, 255, 0.6);
	font-size: 24px;
	cursor: pointer;
}

.modal-body {
	padding: 24px;
}

.summary-card {
	background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.2));
	border-radius: 12px;
	padding: 20px;
	margin-bottom: 24px;
}

.summary-row {
	display: flex;
	justify-content: space-around;
}

.summary-item {
	text-align: center;
}

.summary-value {
	display: block;
	font-size: 24px;
	font-weight: 700;
	color: white;
}

.summary-label {
	display: block;
	font-size: 12px;
	color: rgba(255, 255, 255, 0.6);
	margin-top: 4px;
}

.activity-section {
	margin-bottom: 24px;
}

.activity-section h4 {
	color: rgba(255, 255, 255, 0.6);
	font-size: 12px;
	text-transform: uppercase;
	letter-spacing: 0.5px;
	margin-bottom: 12px;
}

.activity-list {
	display: flex;
	flex-direction: column;
	gap: 8px;
}

.activity-item {
	display: flex;
	align-items: center;
	gap: 12px;
	padding: 12px;
	background: rgba(255, 255, 255, 0.05);
	border-radius: 8px;
	cursor: pointer;
	transition: background 0.2s;
}

.activity-item:hover {
	background: rgba(255, 255, 255, 0.1);
}

.activity-icon {
	width: 36px;
	height: 36px;
	border-radius: 50%;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 16px;
	background: rgba(255, 255, 255, 0.1);
}

.activity-content {
	flex: 1;
}

.activity-title {
	color: white;
	font-weight: 500;
}

.activity-meta {
	display: flex;
	gap: 12px;
	font-size: 12px;
	color: rgba(255, 255, 255, 0.5);
}

.activity-amount {
	font-weight: 600;
	font-size: 14px;
}

.activity-amount.positive {
	color: #22c55e;
}

.activity-amount.negative {
	color: #ef4444;
}

.empty-state {
	text-align: center;
	padding: 24px;
	color: rgba(255, 255, 255, 0.5);
}

.session-section {
	background: rgba(255, 255, 255, 0.05);
	border-radius: 8px;
	padding: 16px;
}

.session-section h4 {
	color: rgba(255, 255, 255, 0.6);
	font-size: 12px;
	text-transform: uppercase;
	letter-spacing: 0.5px;
	margin-bottom: 12px;
}

.session-info {
	display: flex;
	flex-direction: column;
	gap: 8px;
}

.session-row {
	display: flex;
	justify-content: space-between;
	color: rgba(255, 255, 255, 0.8);
	font-size: 14px;
}

.modal-footer {
	display: flex;
	justify-content: flex-end;
	gap: 12px;
	padding: 16px 24px;
	border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.btn {
	padding: 10px 20px;
	border-radius: 8px;
	font-weight: 600;
	cursor: pointer;
	transition: all 0.2s;
	text-decoration: none;
	display: inline-block;
}

.btn-primary {
	background: #3b82f6;
	color: white;
	border: none;
}

.btn-primary:hover {
	background: #2563eb;
}

.btn-secondary {
	background: transparent;
	color: rgba(255, 255, 255, 0.8);
	border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover {
	background: rgba(255, 255, 255, 0.1);
}
</style>
