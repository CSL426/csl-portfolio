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
  <header class="sticky top-0 z-30 flex justify-center px-[0.75rem] pt-[0.875rem] narrow:px-[0.5rem]">
    <!-- N5 floating pill: content-sized and detached from the edges. -->
    <nav
      aria-label="主要導覽"
      class="flex min-w-0 max-w-[min(44rem,100%)] items-center gap-[0.5rem] rounded-full border border-rule bg-paper-2 py-[0.3125rem] pl-[0.875rem] pr-[0.3125rem] narrow:gap-[0.25rem] narrow:pl-[0.625rem] narrow:pr-[0.25rem] shadow-[0_0.5rem_1.5rem_-0.75rem_var(--color-shadow)] sm:gap-[1.5rem] sm:pl-[1.125rem]"
    >
      <RouterLink
        to="/"
        class="shrink-0 whitespace-nowrap rounded-[var(--radius-control)] font-display text-[0.875rem] font-bold tracking-[-0.01em] text-ink narrow:text-[0.8125rem] sm:text-[1rem]"
      >
        <!-- The narrowest phones drop ".dev" so all four links still fit on one line. -->
        Spark<span class="tiny:hidden"><span class="text-accent">.</span>dev</span>
      </RouterLink>
      <!-- With a large browser text size the links scroll inside the pill instead of
           running off screen, where overflow-x: clip would hide them for good. -->
      <ul class="flex min-w-0 items-center gap-[0.125rem] overflow-x-auto [scrollbar-width:none]">
        <li v-for="link in links" :key="link.to">
          <RouterLink
            :to="link.to"
            :aria-current="isActive(link.to) ? 'page' : undefined"
            class="block whitespace-nowrap rounded-full px-[0.5rem] py-[0.3125rem] text-[0.75rem] narrow:px-[0.375rem] tiny:px-[0.3125rem] font-medium transition-colors duration-[180ms] ease-[var(--ease-out)] sm:px-[0.875rem] sm:text-[0.875rem]"
            :class="
              isActive(link.to)
                ? 'bg-ink text-on-ink'
                : 'text-ink-2 hover:bg-surface-subtle hover:text-ink'
            "
          >
            {{ link.label }}
          </RouterLink>
        </li>
      </ul>
    </nav>
  </header>
</template>
