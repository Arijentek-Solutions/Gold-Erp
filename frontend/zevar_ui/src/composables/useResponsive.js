/**
 * Responsive Design Utilities Com *
 * Provides reactive design detection and grid utilities.
 */

import { ref, onMounted, onUnmounted, computed } from 'vue'

const windowWidth = ref(0)
const windowHeight = ref(0)
const isMobile = ref(false)
const isTablet = ref(false)
const isDesktop = ref(false)
const isLargeDesktop = ref(false)
const orientation = ref('portrait')
const isTouchDevice = ref(false)

// Breakpoint definitions
const BREAKPOINTS = {
	mobile: 639,
	tablet: 1024,
	desktop: 1280,
	largeDesktop: 1920,
}

function useResponsive() {
	// Update dimensions on resize
	function updateDimensions() {
		windowWidth.value = window.innerWidth
		windowHeight.value = window.innerHeight

		// Update touch device detection
		isTouchDevice.value = 'ontouchstart' in window || navigator.maxTouchPoints > 0

		if (windowWidth.value < BREAKPOINTS.tablet) {
			isMobile.value = true
			isTablet.value = false
			isDesktop.value = false
			isLargeDesktop.value = false
			orientation.value = 'portrait'
		} else if (windowWidth.value < BREAKPOINTS.desktop) {
			isMobile.value = false
			isTablet.value = true
			isDesktop.value = false
			isLargeDesktop.value = false
			orientation.value = 'landscape'
		} else if (windowWidth.value < BREAKPOINTS.largeDesktop) {
			isMobile.value = false
			isTablet.value = false
			isDesktop.value = true
			isLargeDesktop.value = false
			orientation.value = 'landscape'
		} else {
			isMobile.value = false
			isTablet.value = false
			isDesktop.value = true
			isLargeDesktop.value = true
			orientation.value = 'landscape'
		}
	}

	// Grid columns based on device
	const gridColumns = computed(() => {
		if (isMobile.value) return 1
		if (isTablet.value) return 2
		if (isDesktop.value) return 3
		return 4
	})

	// Safe area insets (for notched devices)
	const safeAreaInsets = computed(() => {
		const style = getComputedStyle(document.documentElement)
		return {
			top: parseInt(style.getProperty('--safe-area-inset-top') || '0px'),
			bottom: parseInt(style.getProperty('--safe-area-inset-bottom') || '0px'),
			left: parseInt(style.getProperty('--safe-area-inset-left') || '0px'),
			right: parseInt(style.getProperty('--safe-area-inset-right') || '0px'),
		}
	})

	onMounted(() => {
		updateDimensions()
		window.addEventListener('resize', updateDimensions)
		// Detect orientation changes
		window.addEventListener('orientationchange', updateDimensions)
	})

	onUnmounted(() => {
		window.removeEventListener('resize', updateDimensions)
		window.removeEventListener('orientationchange', updateDimensions)
	})

	return {
		// Dimensions
		windowWidth,
		windowHeight,
		// Device flags
		isMobile,
		isTablet,
		isDesktop,
		isLargeDesktop,
		// Computed
		orientation,
		gridColumns,
		isTouchDevice,
		safeAreaInsets,
	}
}

// CSS class helpers for responsive design
export const responsiveClasses = computed(() => ({
	mobile: isMobile.value,
	tablet: isTablet.value,
	desktop: isDesktop.value,
	largeDesktop: isLargeDesktop.value,
	touch: isTouchDevice.value,
	portrait: orientation.value === 'portrait',
	landscape: orientation.value === 'landscape',
}))

export default useResponsive
