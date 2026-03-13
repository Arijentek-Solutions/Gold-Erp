<template>
	<div v-if="show" class="modal-overlay" @click.self="close">
		<div class="modal-content">
			<div class="modal-header">
				<h2>POS Preferences</h2>
				<button class="close-btn" @click="close">&times;</button>
			</div>

			<div class="modal-body">
				<!-- Default Behavior -->
				<div class="settings-section">
					<h4>Default Behavior</h4>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Auto-print Receipt</span>
							<span class="setting-desc"
								>Automatically print receipt after each sale</span
							>
						</div>
						<label class="toggle">
							<input
								type="checkbox"
								v-model="prefs.auto_print_receipt"
								@change="savePrefs"
							/>
							<span class="toggle-slider"></span>
						</label>
					</div>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Auto-email Receipt</span>
							<span class="setting-desc">Send receipt to customer email</span>
						</div>
						<label class="toggle">
							<input
								type="checkbox"
								v-model="prefs.auto_email_receipt"
								@change="savePrefs"
							/>
							<span class="toggle-slider"></span>
						</label>
					</div>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Ask for Customer</span>
							<span class="setting-desc"
								>Prompt to select customer before checkout</span
							>
						</div>
						<label class="toggle">
							<input
								type="checkbox"
								v-model="prefs.ask_for_customer"
								@change="savePrefs"
							/>
							<span class="toggle-slider"></span>
						</label>
					</div>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Confirm Void</span>
							<span class="setting-desc">Require confirmation before voiding</span>
						</div>
						<label class="toggle">
							<input
								type="checkbox"
								v-model="prefs.confirm_void"
								@change="savePrefs"
							/>
							<span class="toggle-slider"></span>
						</label>
					</div>
				</div>

				<!-- Receipt Settings -->
				<div class="settings-section">
					<h4>Receipt Settings</h4>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Receipt Format</span>
						</div>
						<select v-model="prefs.receipt_format" @change="savePrefs">
							<option value="thermal">Thermal (80mm)</option>
							<option value="standard">Standard (A4)</option>
							<option value="compact">Compact</option>
						</select>
					</div>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Show Tax Breakdown</span>
							<span class="setting-desc">Display tax details on receipt</span>
						</div>
						<label class="toggle">
							<input
								type="checkbox"
								v-model="prefs.show_tax_breakdown"
								@change="savePrefs"
							/>
							<span class="toggle-slider"></span>
						</label>
					</div>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Print Item Details</span>
							<span class="setting-desc">Include item descriptions on receipt</span>
						</div>
						<label class="toggle">
							<input
								type="checkbox"
								v-model="prefs.print_item_details"
								@change="savePrefs"
							/>
							<span class="toggle-slider"></span>
						</label>
					</div>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Receipt Footer</span>
							<span class="setting-desc">Custom message on receipts</span>
						</div>
						<input
							type="text"
							v-model="prefs.receipt_footer"
							placeholder="Thank you for shopping with us!"
							@change="savePrefs"
							class="text-input"
						/>
					</div>
				</div>

				<!-- Payment Defaults -->
				<div class="settings-section">
					<h4>Payment Defaults</h4>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Default Payment Method</span>
						</div>
						<select v-model="prefs.default_payment_method" @change="savePrefs">
							<option value="Cash">Cash</option>
							<option value="Credit Card">Credit Card</option>
							<option value="Debit Card">Debit Card</option>
						</select>
					</div>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Round to Nearest</span>
						</div>
						<select v-model="prefs.rounding" @change="savePrefs">
							<option value="0.01">Cent</option>
							<option value="0.05">Nickel</option>
							<option value="0.10">Dime</option>
							<option value="0.25">Quarter</option>
							<option value="1.00">Dollar</option>
						</select>
					</div>
				</div>

				<!-- Quick Keys -->
				<div class="settings-section">
					<h4>Quick Cash Amounts</h4>
					<div class="quick-amounts">
						<button
							v-for="amount in quickAmounts"
							:key="amount"
							class="amount-chip"
							:class="{ active: prefs.quick_amounts?.includes(amount) }"
							@click="toggleQuickAmount(amount)"
						>
							${{ amount }}
						</button>
					</div>
					<p class="hint">Click to toggle quick cash buttons</p>
				</div>
			</div>

			<div class="modal-footer">
				<button class="btn btn-secondary" @click="resetPrefs">Reset to Defaults</button>
				<button class="btn btn-primary" @click="close">Done</button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
	show: { type: Boolean, default: false },
})

const emit = defineEmits(['close'])

const defaultPrefs = {
	auto_print_receipt: true,
	auto_email_receipt: false,
	ask_for_customer: true,
	confirm_void: true,
	receipt_format: 'thermal',
	show_tax_breakdown: true,
	print_item_details: false,
	receipt_footer: 'Thank you for shopping with us!',
	default_payment_method: 'Cash',
	rounding: '0.01',
	quick_amounts: [5, 10, 20, 50, 100],
}

const prefs = ref({ ...defaultPrefs })
const quickAmounts = [1, 5, 10, 20, 50, 100, 200, 500]

function savePrefs() {
	localStorage.setItem('pos_preferences', JSON.stringify(prefs.value))
}

function loadPrefs() {
	const stored = localStorage.getItem('pos_preferences')
	if (stored) {
		try {
			prefs.value = { ...defaultPrefs, ...JSON.parse(stored) }
		} catch {
			prefs.value = { ...defaultPrefs }
		}
	}
}

function resetPrefs() {
	prefs.value = { ...defaultPrefs }
	savePrefs()
}

function toggleQuickAmount(amount) {
	if (!prefs.value.quick_amounts) {
		prefs.value.quick_amounts = []
	}
	const index = prefs.value.quick_amounts.indexOf(amount)
	if (index > -1) {
		prefs.value.quick_amounts.splice(index, 1)
	} else {
		prefs.value.quick_amounts.push(amount)
		prefs.value.quick_amounts.sort((a, b) => a - b)
	}
	savePrefs()
}

function close() {
	emit('close')
}

watch(
	() => props.show,
	(val) => {
		if (val) loadPrefs()
	}
)

onMounted(loadPrefs)
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

.settings-section {
	margin-bottom: 24px;
}

.settings-section h4 {
	color: rgba(255, 255, 255, 0.6);
	font-size: 12px;
	text-transform: uppercase;
	letter-spacing: 0.5px;
	margin-bottom: 12px;
}

.setting-item {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 12px 0;
	border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.setting-info {
	flex: 1;
}

.setting-label {
	display: block;
	color: white;
	font-weight: 500;
}

.setting-desc {
	display: block;
	color: rgba(255, 255, 255, 0.5);
	font-size: 12px;
	margin-top: 2px;
}

.toggle {
	position: relative;
	display: inline-block;
	width: 48px;
	height: 24px;
}

.toggle input {
	opacity: 0;
	width: 0;
	height: 0;
}

.toggle-slider {
	position: absolute;
	cursor: pointer;
	inset: 0;
	background: rgba(255, 255, 255, 0.2);
	border-radius: 24px;
	transition: 0.3s;
}

.toggle-slider::before {
	position: absolute;
	content: '';
	height: 18px;
	width: 18px;
	left: 3px;
	bottom: 3px;
	background: white;
	border-radius: 50%;
	transition: 0.3s;
}

.toggle input:checked + .toggle-slider {
	background: #3b82f6;
}

.toggle input:checked + .toggle-slider::before {
	transform: translateX(24px);
}

select,
.text-input {
	padding: 8px 12px;
	background: rgba(255, 255, 255, 0.1);
	border: 1px solid rgba(255, 255, 255, 0.2);
	border-radius: 6px;
	color: white;
	min-width: 120px;
}

.text-input {
	flex: 1;
	max-width: 200px;
}

.quick-amounts {
	display: flex;
	flex-wrap: wrap;
	gap: 8px;
}

.amount-chip {
	padding: 8px 16px;
	background: rgba(255, 255, 255, 0.1);
	border: 2px solid rgba(255, 255, 255, 0.1);
	border-radius: 20px;
	color: white;
	cursor: pointer;
	transition: all 0.2s;
}

.amount-chip:hover {
	border-color: rgba(59, 130, 246, 0.5);
}

.amount-chip.active {
	background: rgba(59, 130, 246, 0.2);
	border-color: #3b82f6;
}

.hint {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.5);
	margin-top: 8px;
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
