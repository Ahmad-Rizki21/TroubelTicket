import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // Proxy all API requests starting with /api to the backend server
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        // Rewrite the path to remove the /api prefix before forwarding
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    }
  }
})
