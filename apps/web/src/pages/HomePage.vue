<script setup lang="ts">
import { RouterLink } from 'vue-router'

const highlights = [
  {
    title: '履歷',
    desc: '完整中英雙語履歷,可線上瀏覽或下載 PDF / PNG。',
    to: '/resume',
    cta: '查看履歷 →',
  },
  {
    title: 'AI Agents',
    desc: '我打造的 AI 助手實驗集合,未來陸續上架。',
    to: '/agents',
    cta: '探索 Agents →',
  },
]
</script>

<template>
  <section class="mx-auto max-w-[64rem] px-[1.25rem] py-[4rem]">
    <div class="mb-[3rem] text-center">
      <p class="mb-[0.75rem] text-[0.875rem] tracking-[0.3em] text-brand-muted">PORTFOLIO</p>
      <h1 class="text-[clamp(2rem,5vw,3.25rem)] font-bold leading-tight">
        Hi, 我是 <span
          class="bg-gradient-to-r from-brand-start to-brand-end bg-clip-text text-transparent"
        >廖啓舜 (Spark)</span>
      </h1>
      <p
        class="mx-auto mt-[1rem] max-w-[40rem] text-[1rem] leading-[1.8] text-brand-muted"
      >
        AI 工程師 · 太空科學碩士 · 對工程與研究都有熱情。這裡是我履歷、專案、與 AI Agent
        實驗的集中地。
      </p>
    </div>

    <div class="grid gap-[1.5rem] md:grid-cols-2">
      <RouterLink
        v-for="h in highlights"
        :key="h.to"
        :to="h.to"
        class="group block rounded-[1.5rem] bg-white p-[2rem] shadow-card transition hover:-translate-y-[0.25rem] hover:shadow-page"
      >
        <h2 class="mb-[0.5rem] text-[1.375rem] font-bold">{{ h.title }}</h2>
        <p class="mb-[1rem] text-[0.9375rem] leading-[1.7] text-brand-muted">{{ h.desc }}</p>
        <span class="text-[0.9375rem] font-medium text-brand-start group-hover:underline">
          {{ h.cta }}
        </span>
      </RouterLink>
    </div>
  </section>
</template>
