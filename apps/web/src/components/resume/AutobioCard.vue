<script setup lang="ts">
import type { AutobiographySection } from '@/types/resume'

defineProps<{ sections: AutobiographySection[] }>()
</script>

<template>
  <div class="flex flex-col gap-[1.625rem]">
    <article
      v-for="(s, i) in sections"
      :key="i"
      class="rounded-[1.875rem] px-[2.25rem] py-[1.875rem]"
      style="background: #f4f8ff; box-shadow: 0 0.875rem 1.625rem rgba(0, 0, 0, 0.08)"
    >
      <h3 class="m-0 mb-[1rem] text-[1.0625rem] font-bold tracking-[0.08em] text-brand-ink">【{{ s.heading }}】</h3>
      <p
        v-for="(p, pi) in s.paragraphs"
        :key="pi"
        class="m-0 mb-[0.875rem] text-[0.9375rem] leading-[1.8] text-brand-muted last:mb-0"
      >
        {{ p }}
      </p>
    </article>
  </div>
</template>
