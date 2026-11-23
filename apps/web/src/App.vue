<script setup lang="ts">
import { RouterLink } from 'vue-router'
import AppNav from '@/components/ui/AppNav.vue'

const year = new Date().getFullYear()

// Plain list, not a <nav>: the primary nav is the only <nav> on the page.
const footerLinks = [
  { to: '/resume', label: 'Resume' },
  { to: '/projects', label: 'Projects' },
  { to: '/agents', label: 'Agents' },
]
</script>

<template>
  <div class="flex min-h-screen flex-col">
    <AppNav class="no-print" />
    <main class="flex-1">
      <RouterView />
    </main>
    <footer class="no-print mx-auto w-full max-w-[64rem] px-[1.25rem] pb-[2rem] pt-[3rem]">
      <div
        class="flex flex-wrap items-center justify-between gap-x-[1.5rem] gap-y-[0.5rem] border-t border-rule pt-[1rem] text-[0.8125rem] text-ink-2"
      >
        <p>© {{ year }} 廖啓舜 · Spark</p>
        <ul class="flex items-center gap-[1rem]">
          <li v-for="link in footerLinks" :key="link.to">
            <RouterLink
              :to="link.to"
              class="whitespace-nowrap rounded-[var(--radius-control)] text-accent underline-offset-4 transition-colors duration-[180ms] ease-[var(--ease-out)] hover:underline"
            >
              {{ link.label }}
            </RouterLink>
          </li>
        </ul>
      </div>
    </footer>
  </div>
</template>
