<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { projects } from '@/data/projects'

const featured = projects.find((p) => p.featured)

// Facts already published elsewhere on the site; nothing here is new copy.
const specRows = [
  { label: '身分', value: 'AI 工程師', mono: false },
  { label: '背景', value: '國立中央大學 太空科學碩士', mono: false },
  { label: '主力專案', value: featured ? featured.name : 'ai-config (acg)', mono: true },
  { label: '即時互動', value: 'Claude Haiku 5.5 · LIVE', mono: true },
]

const linkClass =
  'rounded-[var(--radius-control)] font-medium text-accent underline-offset-4 transition-colors duration-[180ms] ease-[var(--ease-out)] hover:underline'
</script>

<template>
  <section class="mx-auto max-w-[64rem] px-[1.25rem] pb-[2rem] pt-[3.5rem] sm:pt-[5rem]">
    <!-- H2 split diptych: claim on the left, a ruled spec sheet on the right. -->
    <div class="grid gap-[2.5rem] lg:grid-cols-[minmax(0,1.35fr)_minmax(0,1fr)] lg:items-end">
      <div class="min-w-0">
        <h1
          class="font-display text-[clamp(2.75rem,6vw+1rem,5rem)] font-bold leading-[1.02] tracking-[-0.025em] [overflow-wrap:anywhere]"
        >
          廖啓舜<span class="block text-ink-2">Spark</span>
        </h1>
        <p class="mt-[1.25rem] max-w-[34rem] text-[1.0625rem] leading-[1.8] text-ink-2">
          AI 工程師 · 太空科學碩士 · 對工程與研究都有熱情。這裡是我履歷、專案、與 AI Agent 實驗的集中地。
        </p>
        <div class="mt-[2rem] flex flex-wrap gap-[0.75rem]">
          <RouterLink
            to="/resume"
            class="inline-flex items-center whitespace-nowrap rounded-full bg-ink px-[1.375rem] py-[0.625rem] text-[0.9375rem] font-medium text-on-ink transition-colors duration-[180ms] ease-[var(--ease-out)] hover:bg-ink-hover active:translate-y-px"
          >
            查看履歷
          </RouterLink>
          <RouterLink
            to="/projects"
            class="inline-flex items-center whitespace-nowrap rounded-full border border-rule-strong bg-paper-2 px-[1.375rem] py-[0.625rem] text-[0.9375rem] font-medium text-ink transition-colors duration-[180ms] ease-[var(--ease-out)] hover:bg-surface-subtle active:translate-y-px"
          >
            瀏覽專案
          </RouterLink>
        </div>
      </div>

      <dl class="min-w-0 border-t border-ink">
        <div
          v-for="row in specRows"
          :key="row.label"
          class="grid grid-cols-[6rem_minmax(0,1fr)] gap-[1rem] border-b border-rule py-[0.875rem]"
        >
          <dt class="text-[0.8125rem] text-ink-2">{{ row.label }}</dt>
          <dd
            class="min-w-0 text-[0.9375rem] text-ink [overflow-wrap:anywhere]"
            :class="row.mono ? 'font-mono text-[0.875rem]' : ''"
          >
            {{ row.value }}
          </dd>
        </div>
      </dl>
    </div>

    <!-- Asymmetric routing: one wide entry, two stacked ones. -->
    <div class="mt-[4rem] grid border-t border-rule lg:grid-cols-[minmax(0,1.35fr)_minmax(0,1fr)]">
      <div class="min-w-0 py-[2rem] lg:border-r lg:border-rule lg:pr-[2.5rem]">
        <h2 class="font-display text-[1.75rem] font-bold tracking-[-0.015em]">
          {{ featured ? featured.name : '專案作品' }}
        </h2>
        <p v-if="featured" class="mt-[0.5rem] text-[0.9375rem] text-ink-2">{{ featured.tagline }}</p>
        <p v-if="featured" class="mt-[1rem] max-w-[38rem] text-[0.9375rem] leading-[1.8]">
          {{ featured.summary }}
        </p>
        <div class="mt-[1.25rem] flex flex-wrap gap-x-[1.25rem] gap-y-[0.5rem] text-[0.9375rem]">
          <RouterLink :to="featured ? `/projects#${featured.id}` : '/projects'" :class="linkClass">
            看這個專案 →
          </RouterLink>
          <RouterLink to="/projects" :class="linkClass">全部專案 →</RouterLink>
        </div>
      </div>

      <div class="grid min-w-0 lg:pl-[2.5rem]">
        <div class="border-t border-rule py-[2rem] lg:border-t-0">
          <h2 class="font-display text-[1.25rem] font-bold">履歷</h2>
          <p class="mt-[0.5rem] text-[0.9375rem] leading-[1.7] text-ink-2">
            中英雙語，可線上瀏覽，也能下載 PDF / PNG；另有給求職系統讀的純文字版。
          </p>
          <div class="mt-[1rem] flex flex-wrap gap-x-[1.25rem] gap-y-[0.5rem] text-[0.9375rem]">
            <RouterLink to="/resume" :class="linkClass">視覺版 →</RouterLink>
            <RouterLink to="/resume/ats" :class="linkClass">ATS 版 →</RouterLink>
          </div>
        </div>
        <div class="border-t border-rule py-[2rem]">
          <h2 class="font-display text-[1.25rem] font-bold">AI Agents 實驗場</h2>
          <p class="mt-[0.5rem] text-[0.9375rem] leading-[1.7] text-ink-2">
            直接問 AI 助理我的經歷與專案，回答都根據這個網站上的履歷資料。
          </p>
          <div class="mt-[1rem] text-[0.9375rem]">
            <RouterLink to="/agents" :class="linkClass">試試看 →</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
