<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <section class="mx-auto max-w-[64rem] px-[1.25rem] pb-[4rem] pt-[5rem]">
    <div class="border-t border-ink pt-[2rem]">
      <p class="font-display text-[clamp(4rem,12vw,8rem)] font-bold leading-none tracking-[-0.03em] text-accent">
        404
      </p>
      <h1 class="mt-[1rem] font-display text-[1.75rem] font-bold">頁面不存在</h1>
      <p class="mt-[0.5rem] text-[0.9375rem] text-ink-2">這個網址可能還沒蓋好。</p>
      <RouterLink
        to="/"
        class="mt-[1.5rem] inline-flex items-center whitespace-nowrap rounded-full bg-ink px-[1.25rem] py-[0.5rem] text-[0.875rem] font-medium text-on-ink transition-colors duration-[180ms] ease-[var(--ease-out)] hover:bg-ink-hover active:translate-y-px"
      >
        回首頁
      </RouterLink>
    </div>
  </section>
</template>
