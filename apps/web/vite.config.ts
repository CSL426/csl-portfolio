import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig(({ mode }) => {
  // Load vars from repo-root .env (one level up from apps/web).
  const repoRoot = fileURLToPath(new URL('../../', import.meta.url))
  const env = { ...loadEnv(mode, repoRoot, ''), ...loadEnv(mode, process.cwd(), '') }

  const vitePort = Number(env.VITE_PORT ?? 5173)
  const apiPort = Number(env.API_PORT ?? 8000)
  const apiTarget = env.VITE_API_PROXY_TARGET ?? `http://localhost:${apiPort}`

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    server: {
      port: vitePort,
      proxy: {
        '/api': {
          target: apiTarget,
          changeOrigin: true,
        },
      },
    },
  }
})
