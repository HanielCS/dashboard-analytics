import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  // CONFIGURAÇÃO DE TESTES (VITEST)
  test: {
    environment: 'jsdom',
    globals: true 
  },
  // CONFIGURAÇÃO DO SERVIDOR (DOCKER)
  server: {
    host: true,
    port: 5173,
    allowedHosts: ['frontend-service', 'localhost', '127.0.0.1'], 
    watch: {
      usePolling: true
    },
    proxy: {
      '/api': {
        target: 'http://backend-service:8000', 
        changeOrigin: true,
        secure: false
      }
    }
  }
})