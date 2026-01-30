import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';
import frappeui from 'frappe-ui/vite';

export default defineConfig({
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
          "X-Frappe-Site-Name": "zevar.localhost"
        }
      }
    }
  },
  plugins: [
    frappeui(),
    vue(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    outDir: `../${path.basename(path.resolve('..'))}/public/frontend`,
    emptyOutDir: true,
    target: 'es2015',
  },
  optimizeDeps: {
    include: ['frappe-ui > feather-icons', 'showdown', 'engine.io-client'],
  },
});