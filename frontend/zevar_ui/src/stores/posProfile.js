/**
 * POS Profile Store
 *
 * Manages POS profile selection and session state.
 */

import { defineStore } from 'pinia'
import { createResource } from 'frappe-ui'
import { ref, computed } from 'vue'

export const usePosProfileStore = defineStore('posProfile', () => {
	// State
	const activeProfile = ref(null)
	const profiles = ref([])
	const loading = ref(false)
	const error = ref(null)

	// Computed
	const hasActiveProfile = computed(() => !!activeProfile.value)
	const profileName = computed(() => activeProfile.value?.name || 'No Profile Selected')
	const warehouse = computed(() => activeProfile.value?.warehouse || null)
	const company = computed(() => activeProfile.value?.company || null)

	// Resources
	const profilesResource = createResource({
		url: 'zevar_core.api.pos_profile.get_pos_profiles',
		auto: false,
		onSuccess(data) {
			profiles.value = data.profiles || []
		},
	})

	const activeProfileResource = createResource({
		url: 'zevar_core.api.pos_profile.get_active_profile',
		auto: true,
		onSuccess(data) {
			if (data.active_profile) {
				activeProfile.value = data.active_profile
				// Persist to localStorage
				localStorage.setItem('pos_profile', JSON.stringify(data.active_profile))
			}
		},
		onError(err) {
			error.value = err.message || 'Failed to load active profile'
		},
	})

	const setActiveProfileResource = createResource({
		url: 'zevar_core.api.pos_profile.set_active_profile',
		auto: false,
		onSuccess(data) {
			if (data.success) {
				// Reload active profile
				activeProfileResource.fetch()
			}
		},
	})

	// Actions
	async function loadProfiles() {
		loading.value = true
		error.value = null
		try {
			await profilesResource.fetch()
		} catch (err) {
			error.value = err.message || 'Failed to load profiles'
		} finally {
			loading.value = false
		}
	}

	async function setActiveProfile(profileName) {
		loading.value = true
		error.value = null
		try {
			await setActiveProfileResource.submit({ profile_name: profileName })
		} catch (err) {
			error.value = err.message || 'Failed to set active profile'
		} finally {
			loading.value = false
		}
	}

	function clearProfile() {
		activeProfile.value = null
		localStorage.removeItem('pos_profile')
	}

	// Initialize from localStorage
	function initFromStorage() {
		const stored = localStorage.getItem('pos_profile')
		if (stored) {
			try {
				activeProfile.value = JSON.parse(stored)
			} catch {
				localStorage.removeItem('pos_profile')
			}
		}
	}

	// Auto-init
	initFromStorage()

	return {
		// State
		activeProfile,
		profiles,
		loading,
		error,

		// Computed
		hasActiveProfile,
		profileName,
		warehouse,
		company,

		// Resources
		profilesResource,
		activeProfileResource,
		setActiveProfileResource,

		// Actions
		loadProfiles,
		setActiveProfile,
		clearProfile,
		initFromStorage,
	}
})
