<script setup lang="ts">
import { projects } from '@/data/projects'
import type { ProjectItem, ProjectStatus } from '@/types/project'

const featured = projects.filter((p) => p.featured)
const others = projects.filter((p) => !p.featured)

const statusMeta: Record<ProjectStatus, { label: string; cls: string }> = {
  active: { label: 'ACTIVE', cls: 'bg-emerald-100 text-emerald-700' },
  live: { label: 'LIVE', cls: 'bg-sky-100 text-sky-700' },
  archived: { label: 'ARCHIVED', cls: 'bg-slate-100 text-slate-600' },
}

function statusOf(p: ProjectItem) {
  return statusMeta[p.status]
}
</script>

<template>
  <section class="mx-auto max-w-[64rem] px-[1.25rem] py-[4rem]">
    <div class="mb-[2.5rem]">
      <p class="mb-[0.5rem] text-[0.875rem] tracking-[0.3em] text-brand-muted">PROJECTS</p>
      <h1 class="text-[clamp(1.75rem,4vw,2.5rem)] font-bold">專案作品</h1>
      <p class="mt-[0.75rem] max-w-[40rem] text-[0.9375rem] leading-[1.8] text-brand-muted">
        從開發者工具到 LINE Bot AI Agent，這些是我獨立完成、實際在用的東西。
      </p>
    </div>

    <!-- Featured -->
    <article
      v-for="p in featured"
      :id="p.id"
      :key="p.id"
      class="mb-[1.5rem] rounded-[1.5rem] bg-white p-[2rem] shadow-card"
    >
      <div class="flex flex-wrap items-start justify-between gap-[0.75rem]">
        <div>
          <div class="flex flex-wrap items-center gap-[0.625rem]">
            <h2 class="text-[1.5rem] font-bold">{{ p.name }}</h2>
            <span
              class="rounded-full px-[0.625rem] py-[0.125rem] text-[0.6875rem] font-medium"
              :class="statusOf(p).cls"
            >
              {{ statusOf(p).label }}
            </span>
          </div>
          <p class="mt-[0.25rem] text-[1rem] text-brand-muted">{{ p.tagline }}</p>
        </div>
        <span class="text-[0.8125rem] text-brand-muted">{{ p.period }}</span>
      </div>

      <p class="mt-[1.25rem] text-[0.9375rem] leading-[1.8]">{{ p.summary }}</p>

      <ul class="mt-[1rem] flex flex-col gap-[0.5rem] text-[0.9375rem] leading-[1.7] text-brand-muted">
        <li v-for="(h, i) in p.highlights" :key="i" class="flex items-start gap-[0.5rem]">
          <span class="mt-[0.6rem] h-[0.375rem] w-[0.375rem] shrink-0 rounded-full bg-brand-start" />
          <span>{{ h }}</span>
        </li>
      </ul>

      <div class="mt-[1.25rem] flex flex-wrap items-center justify-between gap-[0.75rem]">
        <ul class="flex flex-wrap gap-[0.375rem]">
          <li
            v-for="s in p.stack"
            :key="s"
            class="rounded-full bg-brand-sidebar px-[0.625rem] py-[0.125rem] text-[0.75rem] text-brand-ink"
          >
            {{ s }}
          </li>
        </ul>
        <div v-if="p.links?.length" class="flex flex-wrap gap-[0.5rem]">
          <a
            v-for="l in p.links"
            :key="l.href"
            :href="l.href"
            target="_blank"
            rel="noopener noreferrer"
            class="rounded-full bg-brand-ink px-[1rem] py-[0.375rem] text-[0.8125rem] font-medium text-white transition hover:bg-brand-ink/90"
          >
            {{ l.label }} ↗
          </a>
        </div>
      </div>
    </article>

    <!-- Others -->
    <ul class="grid gap-[1.25rem] md:grid-cols-3">
      <li
        v-for="p in others"
        :id="p.id"
        :key="p.id"
        class="flex flex-col rounded-[1.25rem] bg-white p-[1.5rem] shadow-card"
      >
        <div class="mb-[0.5rem] flex items-start justify-between gap-[0.5rem]">
          <h2 class="text-[1.125rem] font-bold">{{ p.name }}</h2>
          <span
            class="shrink-0 rounded-full px-[0.625rem] py-[0.125rem] text-[0.6875rem] font-medium"
            :class="statusOf(p).cls"
          >
            {{ statusOf(p).label }}
          </span>
        </div>
        <p class="text-[0.8125rem] text-brand-muted">{{ p.tagline }} · {{ p.period }}</p>
        <p class="mt-[0.75rem] flex-1 text-[0.875rem] leading-[1.7]">{{ p.summary }}</p>
        <ul class="mt-[1rem] flex flex-wrap gap-[0.375rem]">
          <li
            v-for="s in p.stack"
            :key="s"
            class="rounded-full bg-brand-sidebar px-[0.5rem] py-[0.0625rem] text-[0.6875rem] text-brand-ink"
          >
            {{ s }}
          </li>
        </ul>
        <div v-if="p.links?.length" class="mt-[0.875rem] flex flex-wrap gap-[0.75rem]">
          <a
            v-for="l in p.links"
            :key="l.href"
            :href="l.href"
            target="_blank"
            rel="noopener noreferrer"
            class="text-[0.8125rem] font-medium text-brand-start hover:underline"
          >
            {{ l.label }} ↗
          </a>
        </div>
      </li>
    </ul>
  </section>
</template>
