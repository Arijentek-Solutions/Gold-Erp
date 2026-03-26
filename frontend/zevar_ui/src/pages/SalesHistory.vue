<template>
	<AppLayout>
		<div class="sales-history-page">
			<div class="page-header">
				<h1>Sales History</h1>
				<p>View and manage past transactions</p>
			</div>

		<!-- Filters -->
		<div class="filters-bar">
			<div class="filter-group">
				<label>From</label>
				<input type="date" v-model="filters.from_date" @change="fetchSales" />
			</div>
			<div class="filter-group">
				<label>To</label>
				<input type="date" v-model="filters.to_date" @change="fetchSales" />
			</div>
			<div class="filter-group">
				<label>Customer</label>
				<input
					type="text"
					v-model="filters.customer"
					placeholder="Search customer..."
					@keyup.enter="fetchSales"
				/>
			</div>
			<div class="filter-group">
				<label>Status</label>
				<select v-model="filters.status" @change="fetchSales">
					<option value="">All</option>
					<option value="Paid">Paid</option>
					<option value="Unpaid">Unpaid</option>
					<option value="Overdue">Overdue</option>
					<option value="Cancelled">Cancelled</option>
				</select>
			</div>
			<div class="filter-group">
				<label>Search</label>
				<input
					type="text"
					v-model="filters.search"
					placeholder="Invoice #..."
					@keyup.enter="fetchSales"
				/>
			</div>
			<button class="btn btn-primary" @click="fetchSales" :disabled="loading">
				🔍 Search
			</button>
		</div>

		<!-- Summary Cards -->
		<div class="summary-cards" v-if="summary">
			<div class="summary-card">
				<span class="card-label">Transactions</span>
				<span class="card-value">{{ summary.transaction_count }}</span>
			</div>
			<div class="summary-card highlight">
				<span class="card-label">Total Sales</span>
				<span class="card-value">${{ formatAmount(summary.total_sales) }}</span>
			</div>
			<div class="summary-card">
				<span class="card-label">Average Sale</span>
				<span class="card-value">${{ formatAmount(summary.average_sale) }}</span>
			</div>
			<div class="summary-card">
				<span class="card-label">Customers</span>
				<span class="card-value">{{ summary.unique_customers }}</span>
			</div>
		</div>

		<!-- Sales Table -->
		<div class="table-container">
			<table class="sales-table">
				<thead>
					<tr>
						<th>Invoice #</th>
						<th>Date</th>
						<th>Customer</th>
						<th>Items</th>
						<th>Total</th>
						<th>Status</th>
						<th>Actions</th>
					</tr>
				</thead>
				<tbody>
					<tr v-if="loading">
						<td colspan="7" class="loading-cell">Loading transactions...</td>
					</tr>
					<tr v-else-if="sales.length === 0">
						<td colspan="7" class="empty-cell">No transactions found</td>
					</tr>
					<tr
						v-else
						v-for="sale in sales"
						:key="sale.name"
						@click="viewDetails(sale.name)"
					>
						<td class="invoice-cell">{{ sale.name }}</td>
						<td>{{ formatDate(sale.posting_date) }}</td>
						<td>{{ sale.customer }}</td>
						<td>{{ sale.item_count || 1 }}</td>
						<td class="amount-cell">${{ formatAmount(sale.grand_total) }}</td>
						<td>
							<span class="status-badge" :class="getStatusClass(sale.status)">
								{{ sale.status }}
							</span>
						</td>
						<td>
							<button
								class="action-btn"
								@click.stop="viewDetails(sale.name)"
								title="View Details"
							>
								👁️
							</button>
							<button
								class="action-btn"
								@click.stop="printInvoice(sale.name)"
								title="Print"
							>
								🖨️
							</button>
						</td>
					</tr>
				</tbody>
			</table>
		</div>

		<!-- Pagination -->
		<div class="pagination" v-if="pagination.total_pages > 1">
			<button
				class="page-btn"
				:disabled="pagination.page === 1"
				@click="goToPage(pagination.page - 1)"
			>
				← Prev
			</button>
			<span class="page-info">
				Page {{ pagination.page }} of {{ pagination.total_pages }} ({{
					pagination.total_count
				}}
				total)
			</span>
			<button
				class="page-btn"
				:disabled="pagination.page === pagination.total_pages"
				@click="goToPage(pagination.page + 1)"
			>
				Next →
			</button>
		</div>

		<!-- Transaction Details Modal -->
		<div
			v-if="selectedTransaction"
			class="modal-overlay"
			@click.self="selectedTransaction = null"
		>
			<div class="modal-content transaction-modal">
				<div class="modal-header">
					<h2>Invoice {{ selectedTransaction.invoice.name }}</h2>
					<button class="close-btn" @click="selectedTransaction = null">&times;</button>
				</div>
				<div class="modal-body">
					<div class="details-grid">
						<div class="detail-section">
							<h4>Customer</h4>
							<p>{{ selectedTransaction.invoice.customer }}</p>
						</div>
						<div class="detail-section">
							<h4>Date & Time</h4>
							<p>
								{{ formatDate(selectedTransaction.invoice.posting_date) }}
								{{ selectedTransaction.invoice.posting_time }}
							</p>
						</div>
						<div class="detail-section">
							<h4>Status</h4>
							<span
								class="status-badge"
								:class="getStatusClass(selectedTransaction.invoice.status)"
							>
								{{ selectedTransaction.invoice.status }}
							</span>
						</div>
					</div>

					<h4>Items</h4>
					<table class="items-table">
						<thead>
							<tr>
								<th>Item</th>
								<th>Qty</th>
								<th>Rate</th>
								<th>Amount</th>
							</tr>
						</thead>
						<tbody>
							<tr v-for="item in selectedTransaction.items" :key="item.item_code">
								<td>{{ item.item_name || item.item_code }}</td>
								<td>{{ item.qty }}</td>
								<td>${{ formatAmount(item.rate) }}</td>
								<td>${{ formatAmount(item.amount) }}</td>
							</tr>
						</tbody>
					</table>

					<div class="totals-section">
						<div class="total-row">
							<span>Subtotal:</span>
							<span>${{ formatAmount(selectedTransaction.invoice.subtotal) }}</span>
						</div>
						<div class="total-row" v-if="selectedTransaction.invoice.discount > 0">
							<span>Discount:</span>
							<span>-${{ formatAmount(selectedTransaction.invoice.discount) }}</span>
						</div>
						<div class="total-row">
							<span>Tax:</span>
							<span>${{ formatAmount(selectedTransaction.invoice.tax) }}</span>
						</div>
						<div class="total-row grand-total">
							<span>Grand Total:</span>
							<span
								>${{ formatAmount(selectedTransaction.invoice.grand_total) }}</span
							>
						</div>
					</div>

					<h4>Payments</h4>
					<div class="payments-list">
						<div
							v-for="payment in selectedTransaction.payments"
							:key="payment.mode_of_payment"
							class="payment-item"
						>
							<span>{{ payment.mode_of_payment }}</span>
							<span>${{ formatAmount(payment.amount) }}</span>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button
						class="btn btn-secondary"
						@click="printInvoice(selectedTransaction.invoice.name)"
					>
						🖨️ Print
					</button>
					<button class="btn btn-secondary" @click="selectedTransaction = null">
						Close
					</button>
				</div>
			</div>
		</div>
	</div>
</AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createResource } from 'frappe-ui'
import AppLayout from '@/components/AppLayout.vue'

// State
const loading = ref(false)
const sales = ref([])
const summary = ref(null)
const selectedTransaction = ref(null)
const pagination = ref({ page: 1, total_pages: 1, total_count: 0 })

const filters = ref({
	from_date: getDefaultFromDate(),
	to_date: getDefaultDate(),
	customer: '',
	status: '',
	search: '',
})

// Resources
const salesResource = createResource({
	url: 'zevar_core.api.sales_history.get_sales_history',
	auto: false,
})

const summaryResource = createResource({
	url: 'zevar_core.api.sales_history.get_sales_summary',
	auto: false,
})

const detailsResource = createResource({
	url: 'zevar_core.api.sales_history.get_transaction_details',
	auto: false,
})

// Methods
function getDefaultDate() {
	return new Date().toISOString().split('T')[0]
}

function getDefaultFromDate() {
	const date = new Date()
	date.setDate(date.getDate() - 30)
	return date.toISOString().split('T')[0]
}

function formatAmount(amount) {
	if (!amount) return '0.00'
	return Number(amount).toFixed(2)
}

function formatDate(dateStr) {
	if (!dateStr) return ''
	const date = new Date(dateStr)
	return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

function getStatusClass(status) {
	const classes = {
		Paid: 'status-paid',
		Unpaid: 'status-unpaid',
		Overdue: 'status-overdue',
		Cancelled: 'status-cancelled',
		Return: 'status-return',
	}
	return classes[status] || 'status-default'
}

async function fetchSales() {
	loading.value = true
	try {
		const [salesResult, summaryResult] = await Promise.all([
			salesResource.submit({
				...filters.value,
				page: pagination.value.page,
				page_size: 20,
			}),
			summaryResource.submit({
				from_date: filters.value.from_date,
				to_date: filters.value.to_date,
			}),
		])

		sales.value = salesResult.sales || []
		pagination.value = salesResult.pagination || pagination.value
		summary.value = summaryResult.summary
	} catch (error) {
		console.error('Failed to fetch sales:', error)
	} finally {
		loading.value = false
	}
}

async function viewDetails(invoiceName) {
	try {
		const result = await detailsResource.submit({ invoice_name: invoiceName })
		selectedTransaction.value = result
	} catch (error) {
		console.error('Failed to fetch details:', error)
	}
}

function printInvoice(invoiceName) {
	window.open(`/printview?doctype=Sales Invoice&name=${invoiceName}`, '_blank')
}

function goToPage(page) {
	pagination.value.page = page
	fetchSales()
}

// Lifecycle
onMounted(() => {
	fetchSales()
})
</script>

<style scoped>
.sales-history-page {
	padding: 24px;
	max-width: 1400px;
	margin: 0 auto;
}

.page-header {
	margin-bottom: 24px;
}

.page-header h1 {
	font-size: 28px;
	font-weight: 700;
	color: white;
	margin-bottom: 4px;
}

.page-header p {
	color: rgba(255, 255, 255, 0.6);
}

.filters-bar {
	display: flex;
	flex-wrap: wrap;
	gap: 12px;
	align-items: flex-end;
	margin-bottom: 24px;
	padding: 16px;
	background: rgba(255, 255, 255, 0.05);
	border-radius: 12px;
}

.filter-group {
	display: flex;
	flex-direction: column;
	gap: 4px;
}

.filter-group label {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.6);
}

.filter-group input,
.filter-group select {
	padding: 8px 12px;
	background: rgba(255, 255, 255, 0.1);
	border: 1px solid rgba(255, 255, 255, 0.2);
	border-radius: 6px;
	color: white;
	min-width: 120px;
}

.summary-cards {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
	gap: 16px;
	margin-bottom: 24px;
}

.summary-card {
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 12px;
	padding: 16px;
	text-align: center;
}

.summary-card.highlight {
	background: rgba(59, 130, 246, 0.1);
	border-color: rgba(59, 130, 246, 0.3);
}

.card-label {
	display: block;
	font-size: 12px;
	color: rgba(255, 255, 255, 0.6);
	margin-bottom: 8px;
}

.card-value {
	display: block;
	font-size: 24px;
	font-weight: 700;
	color: white;
}

.table-container {
	background: rgba(255, 255, 255, 0.05);
	border-radius: 12px;
	overflow: hidden;
}

.sales-table {
	width: 100%;
	border-collapse: collapse;
}

.sales-table th {
	padding: 16px 12px;
	text-align: left;
	font-size: 12px;
	font-weight: 600;
	color: rgba(255, 255, 255, 0.6);
	text-transform: uppercase;
	background: rgba(255, 255, 255, 0.05);
	border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sales-table td {
	padding: 16px 12px;
	color: white;
	border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.sales-table tbody tr {
	cursor: pointer;
	transition: background 0.2s;
}

.sales-table tbody tr:hover {
	background: rgba(255, 255, 255, 0.05);
}

.loading-cell,
.empty-cell {
	text-align: center;
	color: rgba(255, 255, 255, 0.5);
	padding: 48px !important;
}

.invoice-cell {
	font-weight: 600;
	color: #3b82f6;
}

.amount-cell {
	font-weight: 600;
	color: #22c55e;
}

.status-badge {
	display: inline-block;
	padding: 4px 8px;
	border-radius: 4px;
	font-size: 12px;
	font-weight: 500;
}

.status-paid {
	background: rgba(34, 197, 94, 0.2);
	color: #22c55e;
}
.status-unpaid {
	background: rgba(251, 191, 36, 0.2);
	color: #fbbf24;
}
.status-overdue {
	background: rgba(239, 68, 68, 0.2);
	color: #ef4444;
}
.status-cancelled {
	background: rgba(107, 114, 128, 0.2);
	color: #9ca3af;
}

.action-btn {
	background: transparent;
	border: none;
	padding: 4px 8px;
	cursor: pointer;
	opacity: 0.6;
	transition: opacity 0.2s;
}

.action-btn:hover {
	opacity: 1;
}

.pagination {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 16px;
	margin-top: 24px;
}

.page-btn {
	padding: 8px 16px;
	background: rgba(255, 255, 255, 0.1);
	border: 1px solid rgba(255, 255, 255, 0.2);
	border-radius: 6px;
	color: white;
	cursor: pointer;
}

.page-btn:disabled {
	opacity: 0.5;
	cursor: not-allowed;
}

.page-info {
	color: rgba(255, 255, 255, 0.6);
	font-size: 14px;
}

/* Modal */
.modal-overlay {
	position: fixed;
	inset: 0;
	background: rgba(0, 0, 0, 0.7);
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 1000;
}

.transaction-modal {
	max-width: 700px;
	max-height: 90vh;
	overflow-y: auto;
}

.modal-content {
	background: #1e293b;
	border-radius: 16px;
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

.details-grid {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	gap: 16px;
	margin-bottom: 24px;
}

.detail-section h4 {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.6);
	margin-bottom: 4px;
}

.detail-section p {
	color: white;
	font-weight: 500;
}

.items-table {
	width: 100%;
	margin-bottom: 24px;
}

.items-table th,
.items-table td {
	padding: 8px 12px;
	text-align: left;
	border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.items-table th {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.6);
}

.totals-section {
	background: rgba(255, 255, 255, 0.05);
	border-radius: 8px;
	padding: 16px;
	margin-bottom: 24px;
}

.total-row {
	display: flex;
	justify-content: space-between;
	padding: 8px 0;
	color: rgba(255, 255, 255, 0.8);
}

.grand-total {
	font-weight: 700;
	font-size: 18px;
	color: white;
	border-top: 1px solid rgba(255, 255, 255, 0.1);
	margin-top: 8px;
	padding-top: 16px;
}

.payments-list {
	display: flex;
	flex-direction: column;
	gap: 8px;
}

.payment-item {
	display: flex;
	justify-content: space-between;
	padding: 8px 12px;
	background: rgba(255, 255, 255, 0.05);
	border-radius: 6px;
	color: white;
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
}

.btn-primary {
	background: #3b82f6;
	color: white;
	border: none;
}

.btn-primary:hover:not(:disabled) {
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

.btn:disabled {
	opacity: 0.6;
	cursor: not-allowed;
}
</style>
