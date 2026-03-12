<template>
	<div class="pos-opening-page">
		<div class="page-header">
			<h1>POS Opening Entry</h1>
			<p>Start your cash register session</p>
		</div>

		<!-- Session Status Check -->
		<div v-if="sessionStatus.has_active_session" class="active-session-warning">
			<div class="warning-icon">⚠️</div>
			<div class="warning-content">
				<h3>Active Session Detected</h3>
				<p>You already have an open session: {{ sessionStatus.session?.name }}</p>
				<p class="session-details">
					Opened: {{ sessionStatus.session?.opening_date }} at {{ sessionStatus.session?.opening_time }}
					| Duration: {{ sessionStatus.session?.duration_hours }}h
					| Sales: {{ sessionStatus.session?.sales_count }}
				</p>
			</div>
			<router-link to="/pos/closing" class="btn btn-primary">
				Go to Closing
			</router-link>
		</div>

		<!-- Opening Form -->
		<div v-else class="opening-form-container">
			<form @submit.prevent="submitOpening" class="opening-form">
				<!-- POS Profile Selection -->
				<div class="form-group">
					<label>POS Profile</label>
					<select v-model="form.pos_profile" required :disabled="loading">
						<option value="">Select a profile...</option>
						<option v-for="profile in profiles" :key="profile.name" :value="profile.name">
							{{ profile.name }} - {{ profile.warehouse }}
						</option>
					</select>
				</div>

				<!-- Opening Balance -->
				<div class="form-group">
					<label>Opening Cash Balance</label>
					<div class="currency-input">
						<span class="currency-symbol">$</span>
						<input
							type="number"
							v-model.number="form.opening_balance"
							step="0.01"
							min="0"
							placeholder="0.00"
							required
							:disabled="loading"
						/>
					</div>
				</div>

				<!-- Cash Breakdown (Optional) -->
				<div class="form-group">
					<label>Cash Breakdown (Optional)</label>
					<div class="breakdown-grid">
						<div v-for="denom in denominations" :key="denom.value" class="breakdown-item">
							<label>${{ denom.value }}</label>
							<input
								type="number"
								v-model.number="form.cash_breakdown[denom.value]"
								min="0"
								placeholder="0"
								@change="calculateTotal"
								:disabled="loading"
							/>
							<span class="subtotal">${{ getSubtotal(denom.value) }}</span>
						</div>
					</div>
					<div class="breakdown-total">
						<span>Calculated Total:</span>
						<strong>${{ calculatedTotal.toFixed(2) }}</strong>
					</div>
				</div>

				<!-- Notes -->
				<div class="form-group">
					<label>Opening Notes (Optional)</label>
					<textarea
						v-model="form.notes"
						placeholder="Any notes for this session..."
						rows="3"
						:disabled="loading"
					></textarea>
				</div>

				<!-- Submit Button -->
				<div class="form-actions">
					<button type="submit" class="btn btn-primary btn-lg" :disabled="loading || !form.pos_profile">
						<span v-if="loading">Opening Session...</span>
						<span v-else>Open Cash Register</span>
					</button>
				</div>
			</form>
		</div>

		<!-- Success Message -->
		<div v-if="successMessage" class="success-overlay">
			<div class="success-card">
				<div class="success-icon">✅</div>
				<h2>Session Opened Successfully!</h2>
				<p>{{ successMessage }}</p>
				<router-link to="/pos" class="btn btn-primary">
					Start Selling
				</router-link>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { createResource } from 'frappe-ui'

// State
const loading = ref(false)
const profiles = ref([])
const sessionStatus = ref({ has_active_session: false })
const successMessage = ref('')
const calculatedTotal = ref(0)

const form = ref({
	pos_profile: '',
	opening_balance: 0,
	cash_breakdown: {},
	notes: ''
})

const denominations = [
	{ value: 100 }, { value: 50 }, { value: 20 }, { value: 10 },
	{ value: 5 }, { value: 1 }, { value: 0.25 }, { value: 0.10 },
	{ value: 0.05 }, { value: 0.01 }
]

// Resources
const profilesResource = createResource({
	url: 'zevar_core.api.pos_profile.get_pos_profiles',
	auto: true,
	onSuccess(data) {
		profiles.value = data.profiles || []
		// Auto-select first profile if only one
		if (profiles.value.length === 1) {
			form.value.pos_profile = profiles.value[0].name
		}
	}
})

const sessionStatusResource = createResource({
	url: 'zevar_core.api.pos_session.get_session_status',
	auto: true,
	onSuccess(data) {
		sessionStatus.value = data
	}
})

const openSessionResource = createResource({
	url: 'zevar_core.api.pos_session.open_pos_session',
	auto: false
})

// Methods
function getSubtotal(denom) {
	const count = form.value.cash_breakdown[denom] || 0
	return (count * denom).toFixed(2)
}

function calculateTotal() {
	let total = 0
	for (const denom of denominations) {
		const count = form.value.cash_breakdown[denom.value] || 0
		total += count * denom.value
	}
	calculatedTotal.value = total
	form.value.opening_balance = total
}

async function submitOpening() {
	loading.value = true
	try {
		const result = await openSessionResource.submit({
			pos_profile: form.value.pos_profile,
			opening_balance: form.value.opening_balance,
			cash_breakdown: Object.entries(form.value.cash_breakdown)
				.filter(([_, count]) => count > 0)
				.map(([denom, count]) => ({
					mode_of_payment: 'Cash',
					denomination: parseFloat(denom),
					count: count,
					amount: count * parseFloat(denom)
				})),
			notes: form.value.notes
		})

		if (result.success) {
			successMessage.value = result.message
		}
	} catch (error) {
		console.error('Failed to open session:', error)
		alert('Failed to open session: ' + (error.message || 'Unknown error'))
	} finally {
		loading.value = false
	}
}

onMounted(() => {
	// Initialize cash breakdown object
	denominations.forEach(d => {
		if (form.value.cash_breakdown[d.value] === undefined) {
			form.value.cash_breakdown[d.value] = 0
		}
	})
})
</script>

<style scoped>
.pos-opening-page {
	padding: 24px;
	max-width: 800px;
	margin: 0 auto;
}

.page-header {
	text-align: center;
	margin-bottom: 32px;
}

.page-header h1 {
	font-size: 28px;
	font-weight: 700;
	color: white;
	margin-bottom: 8px;
}

.page-header p {
	color: rgba(255, 255, 255, 0.6);
}

.active-session-warning {
	display: flex;
	align-items: center;
	gap: 16px;
	padding: 20px;
	background: rgba(251, 191, 36, 0.1);
	border: 1px solid rgba(251, 191, 36, 0.3);
	border-radius: 12px;
	margin-bottom: 24px;
}

.warning-icon {
	font-size: 32px;
}

.warning-content {
	flex: 1;
}

.warning-content h3 {
	color: #fbbf24;
	margin-bottom: 4px;
}

.warning-content p {
	color: rgba(255, 255, 255, 0.7);
	font-size: 14px;
}

.session-details {
	font-size: 12px;
	margin-top: 8px;
}

.opening-form-container {
	background: rgba(255, 255, 255, 0.05);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 16px;
	padding: 24px;
}

.form-group {
	margin-bottom: 24px;
}

.form-group label {
	display: block;
	color: rgba(255, 255, 255, 0.8);
	font-size: 14px;
	font-weight: 500;
	margin-bottom: 8px;
}

.form-group select,
.form-group input[type="number"],
.form-group textarea {
	width: 100%;
	padding: 12px 16px;
	background: rgba(255, 255, 255, 0.1);
	border: 1px solid rgba(255, 255, 255, 0.2);
	border-radius: 8px;
	color: white;
	font-size: 16px;
}

.form-group select:focus,
.form-group input:focus,
.form-group textarea:focus {
	outline: none;
	border-color: #3b82f6;
}

.currency-input {
	position: relative;
}

.currency-symbol {
	position: absolute;
	left: 16px;
	top: 50%;
	transform: translateY(-50%);
	color: rgba(255, 255, 255, 0.5);
}

.currency-input input {
	padding-left: 32px;
}

.breakdown-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
	gap: 12px;
}

.breakdown-item {
	display: flex;
	flex-direction: column;
	gap: 4px;
}

.breakdown-item label {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.6);
}

.breakdown-item input {
	padding: 8px 12px;
}

.subtotal {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.5);
}

.breakdown-total {
	display: flex;
	justify-content: space-between;
	padding: 12px;
	background: rgba(255, 255, 255, 0.05);
	border-radius: 8px;
	margin-top: 12px;
	color: white;
}

.form-actions {
	text-align: center;
	padding-top: 16px;
}

.btn {
	padding: 12px 24px;
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

.btn-primary:hover:not(:disabled) {
	background: #2563eb;
}

.btn:disabled {
	opacity: 0.6;
	cursor: not-allowed;
}

.btn-lg {
	padding: 16px 48px;
	font-size: 18px;
}

.success-overlay {
	position: fixed;
	inset: 0;
	background: rgba(0, 0, 0, 0.8);
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 1000;
}

.success-card {
	background: #1e293b;
	padding: 48px;
	border-radius: 16px;
	text-align: center;
	max-width: 400px;
}

.success-icon {
	font-size: 64px;
	margin-bottom: 16px;
}

.success-card h2 {
	color: white;
	margin-bottom: 8px;
}

.success-card p {
	color: rgba(255, 255, 255, 0.7);
	margin-bottom: 24px;
}
</style>
