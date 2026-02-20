import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import frappeui from 'frappe-ui/vite'

export default defineConfig({
	base: '/assets/zevar_core/pos/',
	server: {
		port: 8080,
		strictPort: true,
		host: true,
		proxy: {
			'^/(app|api|assets|files|private)': {
				target: 'http://127.0.0.1:8000',
				ws: true,
				changeOrigin: true,
				headers: {
					'X-Frappe-Site-Name': 'zevar.localhost',
				},
			},
		},
	},
	plugins: [frappeui(), vue()],
	resolve: {
		alias: {
			'@': path.resolve(__dirname, './src'),
		},
	},
	build: {
		outDir: `../../zevar_core/public/pos`,
		emptyOutDir: true,
		target: 'es2015',
		manifest: true,
	},
	optimizeDeps: {
		include: ['frappe-ui > feather-icons', 'showdown', 'engine.io-client'],
	},
})
