<script setup lang="ts">
import type { EducationItem, ExperienceItem } from '@/types/resume'

defineProps<{
  education: EducationItem[]
  tools?: string[]
  academic?: ExperienceItem[]
}>()
</script>

<template>
  <aside class="rounded-[1.625rem] bg-brand-sidebar p-[1.25rem] shadow-card">
    <section>
      <h3
        class="m-0 mb-[0.625rem] border-b-2 border-black/10 pb-[0.375rem] text-[1.125rem] font-bold tracking-[0.06em]"
      >
        學歷
      </h3>
      <div class="flex flex-col gap-[1rem]">
        <div
          v-for="(item, i) in education"
          :key="i"
          class="flex flex-col text-[0.875rem] leading-[1.4]"
        >
          <strong>{{ item.school }}</strong>
          <strong>{{ item.degree }}</strong>
          <span class="block text-[0.75rem] text-brand-muted">{{ item.period }}</span>
          <p v-if="item.note" class="mt-[0.375rem] text-[0.8125rem] leading-[1.5] text-brand-muted">
            {{ item.note }}
          </p>
        </div>
      </div>
    </section>

    <section v-if="tools?.length" class="mt-[1.125rem]">
      <h3
        class="m-0 mb-[0.5rem] border-b-2 border-black/10 pb-[0.375rem] text-[1.125rem] font-bold tracking-[0.06em]"
      >
        技術工具
      </h3>
      <p class="m-0 text-[0.75rem] leading-[1.55] text-brand-muted">{{ tools.join('、') }}</p>
    </section>

    <section v-if="academic?.length" class="mt-[1.125rem]">
      <h3
        class="m-0 mb-[0.625rem] border-b-2 border-black/10 pb-[0.375rem] text-[1.125rem] font-bold tracking-[0.06em]"
      >
        學術研究
      </h3>
      <div v-for="(item, i) in academic" :key="i" class="text-[0.8125rem] leading-[1.5]">
        <strong class="block text-[0.875rem]">{{ item.title }}</strong>
        <p v-for="(b, bi) in item.bullets" :key="bi" class="mt-[0.375rem] text-brand-muted">
          {{ b }}
        </p>
      </div>
    </section>
  </aside>
</template>
