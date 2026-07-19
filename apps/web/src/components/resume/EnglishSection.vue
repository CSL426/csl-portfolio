<script setup lang="ts">
import type { EnglishSection } from '@/types/resume'

defineProps<{ sections: EnglishSection[] }>()
</script>

<template>
  <div class="flex flex-col gap-[1.25rem]">
    <article
      v-for="(s, i) in sections"
      :key="i"
      class="rounded-[1.875rem] px-[2.25rem] py-[1.375rem]"
      style="background: #f4f8ff; box-shadow: 0 0.875rem 1.625rem rgba(0, 0, 0, 0.08)"
    >
      <h3 class="m-0 mb-[0.75rem] text-[1.0625rem] font-bold tracking-[0.04em] text-brand-ink">
        {{ s.heading }}
      </h3>
      <p
        v-for="(p, pi) in s.paragraphs"
        :key="`p-${pi}`"
        class="m-0 mb-[0.875rem] text-[0.9375rem] leading-[1.8] text-brand-muted last:mb-0"
      >
        {{ p }}
      </p>
      <ul v-if="s.bullets" class="mt-[0.5rem] flex flex-col gap-[0.25rem] list-none p-0">
        <li
          v-for="(b, bi) in s.bullets"
          :key="`b-${bi}`"
          class="flex items-start gap-[0.375rem] text-[0.9375rem] leading-[1.8] text-brand-muted"
        >
          <span class="text-brand-muted select-none">-</span>
          <span class="flex-1">{{ b }}</span>
        </li>
      </ul>
    </article>
  </div>
</template>
