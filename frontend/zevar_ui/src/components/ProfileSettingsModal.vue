<template>
	<div v-if="show" class="modal-overlay" @click.self="close">
		<div class="modal-content">
			<div class="modal-header">
				<h2>Profile Settings</h2>
				<button class="close-btn" @click="close">&times;</button>
			</div>

			<div class="modal-body">
				<!-- User Info -->
				<div class="user-info">
					<div class="avatar">
						{{ userInitials }}
					</div>
					<div class="user-details">
						<h3>{{ user?.full_name || user?.email || 'User' }}</h3>
						<p>{{ user?.email }}</p>
					</div>
				</div>

				<!-- Settings Sections -->
				<div class="settings-section">
					<h4>Display Settings</h4>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Dark Mode</span>
							<span class="setting-desc">Use dark theme throughout the app</span>
						</div>
						<label class="toggle">
							<input
								type="checkbox"
								v-model="settings.dark_mode"
								@change="saveSettings"
							/>
							<span class="toggle-slider"></span>
						</label>
					</div>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Compact View</span>
							<span class="setting-desc">Reduce spacing in lists and cards</span>
						</div>
						<label class="toggle">
							<input
								type="checkbox"
								v-model="settings.compact_view"
								@change="saveSettings"
							/>
							<span class="toggle-slider"></span>
						</label>
					</div>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Currency Display</span>
							<span class="setting-desc">How to show prices</span>
						</div>
						<select v-model="settings.currency_display" @change="saveSettings">
							<option value="symbol">$ Symbol</option>
							<option value="code">USD Code</option>
							<option value="name">US Dollar</option>
						</select>
					</div>
				</div>

				<div class="settings-section">
					<h4>Notification Settings</h4>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Sound Alerts</span>
							<span class="setting-desc">Play sound on order completion</span>
						</div>
						<label class="toggle">
							<input
								type="checkbox"
								v-model="settings.sound_alerts"
								@change="saveSettings"
							/>
							<span class="toggle-slider"></span>
						</label>
					</div>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Low Stock Alerts</span>
							<span class="setting-desc">Alert when items are low in stock</span>
						</div>
						<label class="toggle">
							<input
								type="checkbox"
								v-model="settings.low_stock_alerts"
								@change="saveSettings"
							/>
							<span class="toggle-slider"></span>
						</label>
					</div>
				</div>

				<div class="settings-section">
					<h4>Language & Region</h4>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Language</span>
						</div>
						<select v-model="settings.language" @change="saveSettings">
							<option value="en">English</option>
							<option value="es">Spanish</option>
							<option value="ar">Arabic</option>
						</select>
					</div>

					<div class="setting-item">
						<div class="setting-info">
							<span class="setting-label">Timezone</span>
						</div>
						<select v-model="settings.timezone" @change="saveSettings">
							<option value="America/New_York">Eastern Time</option>
							<option value="America/Chicago">Central Time</option>
							<option value="America/Denver">Mountain Time</option>
							<option value="America/Los_Angeles">Pacific Time</option>
						</select>
					</div>
				</div>
			</div>

			<div class="modal-footer">
				<button class="btn btn-secondary" @click="resetSettings">Reset to Defaults</button>
				<button class="btn btn-primary" @click="close">Done</button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const props = defineProps({
	show: { type: Boolean, default: false },
	user: { type: Object, default: null },
})

const emit = defineEmits(['close'])

const defaultSettings = {
	dark_mode: true,
	compact_view: false,
	currency_display: 'symbol',
	sound_alerts: true,
	low_stock_alerts: true,
	language: 'en',
	timezone: 'America/New_York',
}

const settings = ref({ ...defaultSettings })

const userInitials = computed(() => {
	const name = props.user?.full_name || props.user?.email || 'U'
	return name
		.split(' ')
		.map((n) => n[0])
		.join('')
		.toUpperCase()
		.slice(0, 2)
})

function saveSettings() {
	localStorage.setItem('pos_settings', JSON.stringify(settings.value))
}

function loadSettings() {
	const stored = localStorage.getItem('pos_settings')
	if (stored) {
		try {
			settings.value = { ...defaultSettings, ...JSON.parse(stored) }
		} catch {
			settings.value = { ...defaultSettings }
		}
	}
}

function resetSettings() {
	settings.value = { ...defaultSettings }
	saveSettings()
}

function close() {
	emit('close')
}

watch(
	() => props.show,
	(val) => {
		if (val) loadSettings()
	}
)

onMounted(loadSettings)
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

.user-info {
	display: flex;
	align-items: center;
	gap: 16px;
	padding: 16px;
	background: rgba(255, 255, 255, 0.05);
	border-radius: 12px;
	margin-bottom: 24px;
}

.avatar {
	width: 56px;
	height: 56px;
	background: linear-gradient(135deg, #3b82f6, #8b5cf6);
	border-radius: 50%;
	display: flex;
	align-items: center;
	justify-content: center;
	color: white;
	font-weight: 700;
	font-size: 18px;
}

.user-details h3 {
	color: white;
	margin: 0 0 4px 0;
}

.user-details p {
	color: rgba(255, 255, 255, 0.6);
	margin: 0;
	font-size: 14px;
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

select {
	padding: 8px 12px;
	background: rgba(255, 255, 255, 0.1);
	border: 1px solid rgba(255, 255, 255, 0.2);
	border-radius: 6px;
	color: white;
	min-width: 120px;
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
