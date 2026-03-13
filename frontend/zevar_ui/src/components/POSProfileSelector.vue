<template>
	<div class="pos-profile-selector">
		<!-- Profile Button -->
		<button class="profile-btn" @click="toggleDropdown" :disabled="loading">
			<span class="profile-icon">🏪</span>
			<span class="profile-name">{{ profileStore.profileName }}</span>
			<span class="dropdown-arrow" :class="{ open: showDropdown }">▼</span>
		</button>

		<!-- Dropdown Menu -->
		<div v-if="showDropdown" class="dropdown-menu">
			<div class="dropdown-header">
				<span>Select POS Profile</span>
				<button class="refresh-btn" @click="refreshProfiles" :disabled="loading">
					🔄
				</button>
			</div>

			<div v-if="loading" class="dropdown-loading">Loading profiles...</div>

			<div v-else-if="error" class="dropdown-error">
				{{ error }}
			</div>

			<div v-else-if="profiles.length === 0" class="dropdown-empty">
				No profiles available
			</div>

			<div v-else class="dropdown-list">
				<button
					v-for="profile in profiles"
					:key="profile.name"
					class="profile-option"
					:class="{ active: isActive(profile.name) }"
					@click="selectProfile(profile.name)"
				>
					<span class="option-name">{{ profile.name }}</span>
					<span v-if="profile.warehouse" class="option-warehouse">
						{{ profile.warehouse }}
					</span>
					<span v-if="isActive(profile.name)" class="check-mark">✓</span>
				</button>
			</div>
		</div>

		<!-- Click outside to close -->
		<div v-if="showDropdown" class="dropdown-backdrop" @click="closeDropdown"></div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { usePosProfileStore } from '@/stores/posProfile'

const profileStore = usePosProfileStore()

// Local state
const showDropdown = ref(false)

// Computed
const profiles = computed(() => profileStore.profiles)
const loading = computed(() => profileStore.loading)
const error = computed(() => profileStore.error)

// Methods
function toggleDropdown() {
	showDropdown.value = !showDropdown.value
	if (showDropdown.value && profiles.value.length === 0) {
		profileStore.loadProfiles()
	}
}

function closeDropdown() {
	showDropdown.value = false
}

function isActive(profileName) {
	return profileStore.activeProfile?.name === profileName
}

async function selectProfile(profileName) {
	await profileStore.setActiveProfile(profileName)
	closeDropdown()
}

async function refreshProfiles() {
	await profileStore.loadProfiles()
}

// Close dropdown on escape key
function handleEscape(e) {
	if (e.key === 'Escape' && showDropdown.value) {
		closeDropdown()
	}
}

onMounted(() => {
	document.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
	document.removeEventListener('keydown', handleEscape)
})
</script>

<style scoped>
.pos-profile-selector {
	position: relative;
}

.profile-btn {
	display: flex;
	align-items: center;
	gap: 8px;
	padding: 8px 12px;
	background: rgba(255, 255, 255, 0.1);
	border: 1px solid rgba(255, 255, 255, 0.2);
	border-radius: 8px;
	color: white;
	cursor: pointer;
	transition: all 0.2s;
}

.profile-btn:hover:not(:disabled) {
	background: rgba(255, 255, 255, 0.15);
}

.profile-btn:disabled {
	opacity: 0.6;
	cursor: not-allowed;
}

.profile-icon {
	font-size: 16px;
}

.profile-name {
	font-size: 14px;
	font-weight: 500;
	max-width: 150px;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.dropdown-arrow {
	font-size: 10px;
	transition: transform 0.2s;
}

.dropdown-arrow.open {
	transform: rotate(180deg);
}

.dropdown-menu {
	position: absolute;
	top: calc(100% + 4px);
	right: 0;
	min-width: 280px;
	background: #1e293b;
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 8px;
	box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
	z-index: 100;
	overflow: hidden;
}

.dropdown-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 12px 16px;
	background: rgba(255, 255, 255, 0.05);
	border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	font-size: 12px;
	font-weight: 600;
	text-transform: uppercase;
	letter-spacing: 0.5px;
	color: rgba(255, 255, 255, 0.7);
}

.refresh-btn {
	background: transparent;
	border: none;
	color: rgba(255, 255, 255, 0.7);
	cursor: pointer;
	padding: 4px;
	border-radius: 4px;
	transition: all 0.2s;
}

.refresh-btn:hover:not(:disabled) {
	background: rgba(255, 255, 255, 0.1);
	color: white;
}

.dropdown-loading,
.dropdown-empty,
.dropdown-error {
	padding: 24px 16px;
	text-align: center;
	color: rgba(255, 255, 255, 0.6);
	font-size: 14px;
}

.dropdown-error {
	color: #f87171;
}

.dropdown-list {
	max-height: 300px;
	overflow-y: auto;
}

.profile-option {
	display: flex;
	align-items: center;
	width: 100%;
	padding: 12px 16px;
	background: transparent;
	border: none;
	color: white;
	cursor: pointer;
	transition: all 0.2s;
	text-align: left;
}

.profile-option:hover {
	background: rgba(255, 255, 255, 0.05);
}

.profile-option.active {
	background: rgba(59, 130, 246, 0.2);
}

.option-name {
	flex: 1;
	font-size: 14px;
	font-weight: 500;
}

.option-warehouse {
	font-size: 12px;
	color: rgba(255, 255, 255, 0.5);
	margin-right: 8px;
}

.check-mark {
	color: #22c55e;
	font-weight: bold;
}

.dropdown-backdrop {
	position: fixed;
	inset: 0;
	z-index: 99;
}
</style>
