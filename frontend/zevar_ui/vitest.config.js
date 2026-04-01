import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
	plugins: [vue()],
	css: {
		postcss: {
			plugins: [], // Override postcss.config.cjs — prevents tailwind.config.js from loading frappe-ui
		},
	},
	test: {
		globals: true,
		environment: 'jsdom',
		css: false,
		include: ['tests/**/*.{test,spec}.{js,ts}'],
		coverage: {
			provider: 'v8',
			reporter: ['text', 'json', 'html'],
			include: ['src/**/*.{js,vue}'],
			exclude: ['src/**/*.spec.js', 'src/**/*.test.js'],
		},
		setupFiles: ['tests/setup.js'],
	},
	resolve: {
		alias: {
			'@': fileURLToPath(new URL('./src', import.meta.url)),
		},
	},
})
