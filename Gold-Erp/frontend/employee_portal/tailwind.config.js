module.exports = {
	darkMode: "class",
	presets: [require("frappe-ui/tailwind")],
	content: [
		"./index.html",
		"./src/**/*.{vue,js,ts,jsx,tsx}",
		"./node_modules/frappe-ui/src/components/**/*.{vue,js,ts,jsx,tsx}",
	],
	theme: {
		fontFamily: {
			sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
			portal: ["Plus Jakarta Sans", "sans-serif"],
		},
		extend: {
			colors: {
				primary: "#FCD34D", // Lighter Gold
				"background-light": "#f8f8f5",
				"background-dark": "#05070a",
				"card-bg": "rgba(15, 20, 40, 0.45)",
				"sapphire-deep": "#0a0c1a",
				"emerald-glow": "#10b981",
				"gold-accent": "#fbbf24",
				"diamond-white": "#e2e8f0",
				"glass-border": "rgba(255, 255, 255, 0.15)",
				// Maintaining previous vars for compatibility if needed, or mapping them
				"portal-primary": "#f4c025", // Mapped to Gold
				"portal-bg-dark": "#0a0c1a", // Mapped to Dark
			},
			fontFamily: {
				sans: ["Inter", "sans-serif"],
				display: ["Spline Sans", "sans-serif"],
				serif: ["Cinzel", "serif"],
			},
			borderRadius: {
				xl: "0.75rem",
				"2xl": "1rem",
			},
			boxShadow: {
				"glow-gold": "0 0 20px rgba(244, 192, 37, 0.3)",
				"glow-sapphire": "0 0 25px rgba(10, 12, 26, 0.5)",
			},
		},
	},
	plugins: [],
};
