<template>
	<div class="relative">
		<button
            @click="toggleDropdown"
            :class="[
                'bg-white/10 dark:bg-gray-800 border border-gray-200',
                isOpen ? 'shadow-lg' : 'shadow-sm',
            ]"
            class="flex items-center gap-2 min-w-[200px]"
        >
            <!-- Selected Profile Indicator -->
            <div
                v-if="activeProfile"
                class="flex items-center gap-2"
            >
                <div
                    class="w-2 h-2 rounded-full flex items-center justify-center"
                    :class="[
                        'bg-[#C9A962] text-white',
                        'text-xs font-bold',
                    {{ activeProfile.currency || 'USD' }}
                </div>
                <div class="text-sm text-gray-500">{{ activeProfile.name }}</div>
                <svg
                    class="w-3 h-3 text-gray-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 9l-7 7-7"
                    />
                </svg>
            </div>

            <!-- Dropdown Menu -->
            <Transition name="dropdown">
                <div
                    v-if="isOpen"
                    class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 border border-gray-200 rounded-lg shadow-xl z-10"
                    <div class="py-2">
                        <button
                            v-for="profile in profiles"
                            :key="profile.name"
                            @click="selectProfile(profile)"
                            class="w-full px-3 py-2 text-left text-sm rounded transition-colors"
                            :class="[
                                selectedProfile?.name === profile.name
                                    ? 'bg-[#C9A962] text-white'
                    : 'text-gray-300',
                    selectedProfile?.name === profile.name ? 'font-semibold' : 'font-medium',
                "
            >
                <div class="text-xs text-gray-400">{{ profile.company }}</div>
            </div>
        </div>
    </Transition>
</template>

<script setup>
import { ref, onMounted, from 'frappe-ui'
import { usePOSProfileStore } from '../stores/posProfile'

const props = {
    isDark: {
        type: Boolean,
        default: false,
    },
}

const emit = ['profileSelected'])

const store = usePOSProfileStore()

const isOpen = ref(false)

const toggleDropdown = () => {
    isOpen.value = !isOpen.value
}

const selectProfile = async (profile) => {
    await store.setActiveProfile(profile.name)
    emit('profileSelected', profile)
    isOpen.value = false
}

onMounted(() => {
    store.loadProfiles()
})
</script>
