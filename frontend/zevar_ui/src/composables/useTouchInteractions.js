/**
 * Touch Interactions Composable
 *
 * Provides touch-friendly interactions for mobile/tablet devices.
 */

import { ref, onMounted, onUnmounted } from 'vue'

const touchStart = ref({ x: 0, y: 0 })
const touchEnd = ref({ x: 0, y: 0 })
const isSwiping = ref(false)
const swipeDirection = ref('none')

export function useTouchInteractions(options = {}) {
	const { onSwipeLeft } = options
	const minSwipeDistance = 50
	const maxSwipeTime = 300

	function handleTouchStart(event) {
		const touch = event.touches[0]
		touchStart.value = { x: touch.clientX, y: touch.clientY }
		isSwiping.value = true
	}

	function handleTouchMove(event) {
		if (!isSwiping.value) return
		const touch = event.touches[0]
		touchEnd.value = { x: touch.clientX, y: touch.clientY }
	}

	function handleTouchEnd() {
		if (!isSwiping.value) return
		isSwiping.value = false

		const deltaX = touchEnd.value.x - touchStart.value.x
		const deltaY = touchEnd.value.y - touchStart.value.y

		// Determine swipe direction
		if (Math.abs(deltaX) > Math.abs(deltaY)) {
			// Horizontal swipe
			if (Math.abs(deltaX) > minSwipeDistance) {
				swipeDirection.value = deltaX > 0 ? 'right' : 'left'
				if (swipeDirection.value === 'left' && onSwipeLeft) {
					onSwipeLeft()
				}
			}
		} else {
			// Vertical swipe
			if (Math.abs(deltaY) > minSwipeDistance) {
				swipeDirection.value = deltaY > 0 ? 'down' : 'up'
			}
		}

		// Reset
		swipeDirection.value = 'none'
	}

	// Add haptic feedback (vibration)
	function hapticFeedback() {
		if ('vibrate' in navigator) {
			navigator.vibrate(10)
		}
	}

	// Long press detection
	const longPressTimer = ref(null)
	const isLongPress = ref(false)

	function handleLongPressStart(event) {
		longPressTimer.value = setTimeout(() => {
			isLongPress.value = true
			hapticFeedback()
			// Emit custom event for long press
			document.dispatchEvent(new CustomEvent('longpress', { detail: event }))
		}, 500)
	}

	function handleLongPressEnd() {
		if (longPressTimer.value) {
			clearTimeout(longPressTimer.value)
			longPressTimer.value = null
		}
		isLongPress.value = false
	}

	onMounted(() => {
		document.addEventListener('touchstart', handleTouchStart, { passive: true })
		document.addEventListener('touchmove', handleTouchMove, { passive: true })
		document.addEventListener('touchend', handleTouchEnd, { passive: true })
		document.addEventListener('touchstart', handleLongPressStart, { passive: true })
		document.addEventListener('touchend', handleLongPressEnd, { passive: true })
	})

	onUnmounted(() => {
		document.removeEventListener('touchstart', handleTouchStart)
		document.removeEventListener('touchmove', handleTouchMove)
		document.removeEventListener('touchend', handleTouchEnd)
		document.removeEventListener('touchstart', handleLongPressStart)
		document.removeEventListener('touchend', handleLongPressEnd)
	})

	return {
		touchStart,
		touchEnd,
		isSwiping,
		swipeDirection,
		isLongPress,
		hapticFeedback,
	}
}

export default useTouchInteractions
