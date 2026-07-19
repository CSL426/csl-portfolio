<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <section
    class="mx-auto flex max-w-[40rem] flex-col items-center px-[1.25rem] py-[6rem] text-center"
  >
    <p class="text-[clamp(3rem,10vw,6rem)] font-bold leading-none text-brand-start">404</p>
    <h1 class="mt-[1rem] text-[1.5rem] font-bold">頁面不存在</h1>
    <p class="mt-[0.5rem] text-[0.9375rem] text-brand-muted">這個網址可能還沒蓋好。</p>
    <RouterLink
      to="/"
      class="mt-[1.5rem] rounded-full bg-brand-ink px-[1.25rem] py-[0.5rem] text-[0.875rem] text-white"
    >
      回首頁
    </RouterLink>
  </section>
</template>
