<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

const links = [
  { to: '/', label: 'Home' },
  { to: '/resume', label: 'Resume' },
  { to: '/agents', label: 'AI Agents' },
]

const activePath = computed(() => route.path)
</script>

<template>
  <header
    class="sticky top-0 z-30 w-full border-b border-white/40 bg-white/70 backdrop-blur"
  >
    <nav
      class="mx-auto flex max-w-6xl items-center justify-between px-[1.25rem] py-[0.875rem]"
    >
      <RouterLink
        to="/"
        class="text-[1.125rem] font-bold tracking-wide text-brand-ink hover:opacity-80"
      >
        Spark<span class="text-brand-start">.</span>dev
      </RouterLink>
      <ul class="flex items-center gap-[1.25rem] text-[0.9375rem]">
        <li v-for="link in links" :key="link.to">
          <RouterLink
            :to="link.to"
            class="rounded-full px-[0.875rem] py-[0.375rem] transition"
            :class="
              activePath === link.to
                ? 'bg-brand-ink text-white'
                : 'text-brand-muted hover:bg-brand-sidebar'
            "
          >
            {{ link.label }}
          </RouterLink>
        </li>
      </ul>
    </nav>
  </header>
</template>
