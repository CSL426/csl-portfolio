<script setup lang="ts">
import type { ExperienceItem } from '@/types/resume'

defineProps<{
  experiences?: ExperienceItem[]
  experiencesHeading?: string
  strengths?: string[]
}>()
</script>

<template>
  <div class="flex flex-col gap-[1rem]">
    <article
      v-if="experiences?.length"
      class="rounded-[1.625rem] bg-white px-[1.75rem] py-[1.25rem] shadow-card"
    >
      <h3
        class="m-0 mb-[0.625rem] flex items-baseline justify-between border-b-2 border-black/10 pb-[0.375rem] text-[1.1875rem] font-bold tracking-[0.06em]"
      >
        {{ experiencesHeading ?? '相關經歷' }}
      </h3>
      <ol class="m-0 list-decimal pl-[1.75rem] text-[0.9375rem] leading-[1.65]">
        <li v-for="(exp, i) in experiences" :key="i" class="mb-[0.375rem]">
          <strong class="text-brand-ink">{{ exp.title }}</strong>
          <ul class="mt-[0.25rem] flex flex-col gap-[0.25rem] list-none p-0">
            <li
              v-for="(b, bi) in exp.bullets"
              :key="bi"
              class="flex items-start gap-[0.375rem] text-[0.9375rem] text-brand-muted"
            >
              <span class="text-brand-muted select-none">-</span>
              <span class="flex-1">{{ b }}</span>
            </li>
          </ul>
        </li>
      </ol>
    </article>

    <article
      v-if="strengths?.length"
      class="rounded-[1.625rem] bg-white px-[1.75rem] py-[1.25rem] shadow-card"
    >
      <h3
        class="m-0 mb-[0.625rem] border-b-2 border-black/10 pb-[0.375rem] text-[1.1875rem] font-bold tracking-[0.06em]"
      >
        技術優勢
      </h3>
      <ol class="m-0 list-decimal pl-[1.25rem] text-[0.9375rem] leading-[1.7]">
        <li v-for="(s, i) in strengths" :key="i" class="mb-[0.25rem] last:mb-0">
          {{ s }}
        </li>
      </ol>
    </article>
  </div>
</template>
