<script setup lang="ts">
import { projects } from '@/data/projects'
import type { ProjectItem, ProjectStatus } from '@/types/project'

const featured = projects.filter((p) => p.featured)
const others = projects.filter((p) => !p.featured)

const statusMeta: Record<ProjectStatus, { label: string; cls: string }> = {
  active: { label: 'ACTIVE', cls: 'bg-status-live-bg text-status-live-fg' },
  live: { label: 'LIVE', cls: 'bg-status-live-bg text-status-live-fg' },
  archived: { label: 'ARCHIVED', cls: 'bg-status-muted-bg text-status-muted-fg' },
}

function statusOf(p: ProjectItem) {
  return statusMeta[p.status]
}

const badge = 'rounded-full px-[0.5rem] py-[0.0625rem] font-mono text-[0.6875rem] font-medium'
const stackTag =
  'rounded-[0.375rem] border border-rule bg-paper px-[0.5rem] py-[0.0625rem] font-mono text-[0.75rem] text-ink'
const textLink =
  'whitespace-nowrap rounded-[var(--radius-control)] text-[0.875rem] font-medium text-accent underline-offset-4 transition-colors duration-[180ms] ease-[var(--ease-out)] hover:underline'
</script>

<template>
  <section class="mx-auto max-w-[64rem] px-[1.25rem] pb-[2rem] pt-[3.5rem]">
    <header class="border-b border-rule pb-[1.5rem]">
      <h1 class="font-display text-[clamp(2rem,4vw+0.5rem,3rem)] font-bold tracking-[-0.02em]">
        專案作品
      </h1>
      <p class="mt-[0.5rem] max-w-[40rem] text-[0.9375rem] leading-[1.8] text-ink-2">
        從開發者工具到 LINE Bot AI Agent，這些是我獨立完成、實際在用的東西。
      </p>
    </header>

    <!-- Featured: main column plus a spec side column. -->
    <article
      v-for="p in featured"
      :id="p.id"
      :key="p.id"
      class="mt-[2rem] grid scroll-mt-[5rem] rounded-[var(--radius-card)] border border-rule bg-paper-2 lg:grid-cols-[minmax(0,1.6fr)_minmax(0,1fr)]"
    >
      <div class="min-w-0 p-[1.5rem] sm:p-[2rem]">
        <div class="flex flex-wrap items-center gap-[0.625rem]">
          <h2 class="font-display text-[1.75rem] font-bold tracking-[-0.015em] [overflow-wrap:anywhere]">
            {{ p.name }}
          </h2>
          <span :class="[badge, statusOf(p).cls]">{{ statusOf(p).label }}</span>
        </div>
        <p class="mt-[0.375rem] text-[1rem] text-ink-2">{{ p.tagline }}</p>
        <p class="mt-[1.25rem] text-[0.9375rem] leading-[1.8]">{{ p.summary }}</p>
        <ul class="mt-[1.25rem] flex flex-col border-t border-rule">
          <li
            v-for="(h, i) in p.highlights"
            :key="i"
            class="border-b border-rule py-[0.75rem] text-[0.9375rem] leading-[1.7] text-ink-2"
          >
            {{ h }}
          </li>
        </ul>
      </div>

      <aside
        class="min-w-0 border-t border-rule p-[1.5rem] sm:p-[2rem] lg:border-l lg:border-t-0"
        :aria-label="`${p.name} 規格`"
      >
        <dl class="flex flex-col gap-[1.5rem]">
          <div>
            <dt class="text-[0.8125rem] text-ink-2">期間</dt>
            <dd class="mt-[0.375rem] font-mono text-[0.875rem] tabular-nums">{{ p.period }}</dd>
          </div>
          <div>
            <dt class="text-[0.8125rem] text-ink-2">技術堆疊</dt>
            <dd class="mt-[0.5rem]">
              <ul class="flex flex-wrap gap-[0.375rem]">
                <li v-for="s in p.stack" :key="s" :class="stackTag">{{ s }}</li>
              </ul>
            </dd>
          </div>
          <div v-if="p.links?.length">
            <dt class="text-[0.8125rem] text-ink-2">外部連結</dt>
            <dd class="mt-[0.5rem] flex flex-wrap gap-[0.5rem]">
              <a
                v-for="l in p.links"
                :key="l.href"
                :href="l.href"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center whitespace-nowrap rounded-full bg-ink px-[1rem] py-[0.4375rem] text-[0.8125rem] font-medium text-on-ink transition-colors duration-[180ms] ease-[var(--ease-out)] hover:bg-ink-hover active:translate-y-px"
              >
                {{ l.label }} ↗
              </a>
            </dd>
          </div>
        </dl>
      </aside>
    </article>

    <!-- Others: F3 ruled index, one project per row. -->
    <ul class="mt-[2.5rem] border-t border-ink">
      <li
        v-for="p in others"
        :id="p.id"
        :key="p.id"
        class="grid scroll-mt-[5rem] gap-[0.75rem] border-b border-rule py-[1.5rem] md:grid-cols-[minmax(0,14rem)_minmax(0,1fr)_auto] md:gap-[2rem]"
      >
        <div class="min-w-0">
          <h2 class="font-display text-[1.125rem] font-bold [overflow-wrap:anywhere]">{{ p.name }}</h2>
          <div class="mt-[0.375rem] flex flex-wrap items-center gap-[0.5rem]">
            <span :class="[badge, statusOf(p).cls]">{{ statusOf(p).label }}</span>
            <span class="font-mono text-[0.8125rem] tabular-nums text-ink-2">{{ p.period }}</span>
          </div>
        </div>
        <div class="min-w-0">
          <p class="text-[0.9375rem] font-medium">{{ p.tagline }}</p>
          <p class="mt-[0.375rem] text-[0.875rem] leading-[1.7] text-ink-2">{{ p.summary }}</p>
          <ul class="mt-[0.75rem] flex flex-wrap gap-[0.375rem]">
            <li v-for="s in p.stack" :key="s" :class="stackTag">{{ s }}</li>
          </ul>
        </div>
        <div v-if="p.links?.length" class="flex flex-wrap gap-x-[1rem] gap-y-[0.375rem] md:flex-col md:items-end">
          <a
            v-for="l in p.links"
            :key="l.href"
            :href="l.href"
            target="_blank"
            rel="noopener noreferrer"
            :class="textLink"
          >
            {{ l.label }} ↗
          </a>
        </div>
      </li>
    </ul>
  </section>
</template>
