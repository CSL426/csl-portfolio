<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

const links = [
  { to: '/', label: 'Home' },
  { to: '/resume', label: 'Resume' },
  { to: '/projects', label: 'Projects' },
  { to: '/agents', label: 'Agents' },
]

const activePath = computed(() => route.path)

function isActive(to: string): boolean {
  return activePath.value === to || (to !== '/' && activePath.value.startsWith(to))
}
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
        class="text-[1rem] font-bold tracking-wide text-brand-ink hover:opacity-80 sm:text-[1.125rem]"
      >
        Spark<span class="text-brand-start">.</span>dev
      </RouterLink>
      <ul class="flex items-center gap-[0.125rem] text-[0.8125rem] sm:gap-[1rem] sm:text-[0.9375rem]">
        <li v-for="link in links" :key="link.to">
          <RouterLink
            :to="link.to"
            :aria-current="isActive(link.to) ? 'page' : undefined"
            class="whitespace-nowrap rounded-full px-[0.5rem] py-[0.375rem] transition sm:px-[0.875rem]"
            :class="
              isActive(link.to)
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
