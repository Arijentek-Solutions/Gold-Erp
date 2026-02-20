/**
 * Formatting Composable
 *
 * Shared formatting functions for currency, weight, etc.
 */

export function useFormatters() {
	/**
	 * Format currency value to USD
	 */
	const formatCurrency = (value, options = {}) => {
		if (!value && value !== 0) return '$0.00'

		const defaults = {
			style: 'currency',
			currency: 'USD',
			minimumFractionDigits: options.compact ? 0 : 2,
			maximumFractionDigits: options.compact ? 0 : 2,
		}

		return new Intl.NumberFormat('en-US', { ...defaults, ...options }).format(value)
	}

	/**
	 * Format weight to 3 decimal places
	 */
	const formatWeight = (value, unit = 'g') => {
		if (!value && value !== 0) return `0.000 ${unit}`
		return `${parseFloat(value).toFixed(3)} ${unit}`
	}

	/**
	 * Format percentage
	 */
	const formatPercentage = (value) => {
		if (!value && value !== 0) return '0%'
		return `${parseFloat(value).toFixed(2)}%`
	}

	/**
	 * Format date
	 */
	const formatDate = (date, options = {}) => {
		if (!date) return ''

		const defaults = {
			year: 'numeric',
			month: 'short',
			day: 'numeric',
		}

		return new Intl.DateTimeFormat('en-US', { ...defaults, ...options }).format(new Date(date))
	}

	return {
		formatCurrency,
		formatWeight,
		formatPercentage,
		formatDate,
	}
}
