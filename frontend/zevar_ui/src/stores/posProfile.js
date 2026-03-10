/**
 * POS Profile Store
 *
 * Manages POS profile selection and session state.
 */

import { defineStore } from 'pinia'
import { createResource } from 'frappe-ui'
import { ref, computed } from 'vue'

export const usePOSProfileStore = defineStore('posProfile', () => {
	// State
	const profiles = ref([])
	const activeProfile = ref(null)
	const isLoading = ref(false)
	const error = ref(null)

	// Computed
	const hasProfiles = computed(() => profiles.value.length > 0)
	const activeProfileName = computed(() => activeProfile.value?.name || null)
	const activeWarehouse = computed(() => activeProfile.value?.warehouse || null)

	// Resources
	const profilesResource = createResource({
		url: 'zevar_core.api.get_pos_profiles',
		auto: false,
		onSuccess(data) {
			if (data && data.profiles) {
				profiles.value = data.profiles
			}
		},
		onError(err) {
			error.value = err.message || 'Failed to load profiles'
		},
	})

	const activeProfileResource = createResource({
		url: 'zevar_core.api.get_active_profile',
		auto: false,
		onSuccess(data) {
			if (data && data.active_profile) {
				activeProfile.value = data.active_profile
				// Also store in localStorage for persistence
				localStorage.setItem('active_pos_profile', data.active_profile.name)
			}
		},
	})

	// Actions
	async function loadProfiles() {
		isLoading.value = true
		error.value = null
		try {
			await profilesResource.fetch()
		} finally {
			isLoading.value = false
		}
	}

	async function loadActiveProfile() {
		await activeProfileResource.fetch()
	}

	async function setActiveProfile(profileName) {
		isLoading.value = true
		error.value = null
		try {
			const result = await frappe.call({
				method: 'POST',
				url: 'zevar_core.api.set_active_profile',
				args: { profile_name: profileName },
			})
			if (result.success) {
				activeProfile.value = profiles.value.find(p => p.name === profileName) || null
				localStorage.setItem('active_pos_profile', profileName)
			}
			return result
		} catch (err) {
			error.value = err.message || 'Failed to set profile'
			throw err
		} finally {
			isLoading.value = false
		}
	}

	function clearActiveProfile() {
		activeProfile.value = null
		localStorage.removeItem('active_pos_profile')
	}

	// Initialize - load profiles and active profile
	async function initialize() {
		await loadProfiles()
		// Check localStorage for saved profile
		const savedProfile = localStorage.getItem('active_pos_profile')
		if (savedProfile) {
			// Verify the profile still exists in available profiles
			const exists = profiles.value.some(p => p.name === savedProfile)
			if (exists) {
				await loadActiveProfile()
			} else {
				localStorage.removeItem('active_pos_profile')
			}
		}
	}

	return {
		// State
		profiles,
		activeProfile,
		isLoading,
		error,
		// Computed
		hasProfiles,
		activeProfileName,
		activeWarehouse,
		// Resources
		profilesResource,
		activeProfileResource,
		// Actions
		loadProfiles,
		loadActiveProfile,
		setActiveProfile,
		clearActiveProfile,
		initialize,
	}
})
