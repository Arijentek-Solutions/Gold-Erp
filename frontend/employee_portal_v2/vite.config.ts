import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
        },
    },
    server: {
        port: 8080,
        proxy: {
            '/api': {
                target: 'http://localhost:8080',
                changeOrigin: true,
            },
            '/assets': {
                target: 'http://localhost:8080',
                changeOrigin: true,
            }
        }
    },
    build: {
        outDir: '../zevar_core/public/employee_portal_v2',
        emptyOutDir: true,
    },
})