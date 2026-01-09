module.exports = {
    darkMode: 'class',
    presets: [require('frappe-ui/src/utils/tailwind.config')],
    content: [
        './index.html',
        './src/**/*.{vue,js,ts,jsx,tsx}',
        './node_modules/frappe-ui/src/components/**/*.{vue,js,ts,jsx,tsx}',
    ],
    theme: {
        // We define fontFamily HERE to override defaults, not in 'extend'
        fontFamily: {
            sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
            serif: ['Cinzel', 'ui-serif', 'Georgia', 'serif'],
        },
        extend: {
            // Keep other extensions here if you have them
        },
    },
    plugins: [],
}