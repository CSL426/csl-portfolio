<script setup lang="ts">
import { ref } from 'vue'
import { useChat } from '@/composables/useChat'

interface AgentPreview {
  name: string
  desc: string
  status: 'coming-soon' | 'live'
}

const agents: AgentPreview[] = [
  { name: 'Echo', desc: 'Pipeline 測試,把訊息回傳給你。', status: 'live' },
  {
    name: 'ADK · Gemini',
    desc: '走 Google Agent Development Kit + Gemini 2.5 Flash。',
    status: 'live',
  },
  { name: 'Trip Planner', desc: '基於「路遊憩」的旅遊規劃 Agent。', status: 'coming-soon' },
]

const input = ref('')
const { messages, pending, error, send, clear } = useChat()

async function onSend() {
  const text = input.value
  input.value = ''
  await send(text)
}
</script>

<template>
  <section class="mx-auto max-w-[64rem] px-[1.25rem] py-[4rem]">
    <div class="mb-[2.5rem]">
      <p class="mb-[0.5rem] text-[0.875rem] tracking-[0.3em] text-brand-muted">AI AGENTS</p>
      <h1 class="text-[clamp(1.75rem,4vw,2.5rem)] font-bold">我正在打造的 AI 助手</h1>
      <p class="mt-[0.75rem] max-w-[40rem] text-[0.9375rem] leading-[1.8] text-brand-muted">
        後端走 FastAPI,前端透過 <code>/api/chat</code> 呼叫,LINE bot 共用同一個 Agent 路由。
      </p>
    </div>

    <ul class="mb-[2.5rem] grid gap-[1.25rem] md:grid-cols-3">
      <li
        v-for="a in agents"
        :key="a.name"
        class="rounded-[1.25rem] bg-white p-[1.5rem] shadow-card"
      >
        <div class="mb-[0.75rem] flex items-center justify-between">
          <h2 class="text-[1.125rem] font-bold">{{ a.name }}</h2>
          <span
            class="rounded-full px-[0.625rem] py-[0.125rem] text-[0.6875rem] font-medium"
            :class="
              a.status === 'live'
                ? 'bg-emerald-100 text-emerald-700'
                : 'bg-amber-100 text-amber-700'
            "
          >
            {{ a.status === 'live' ? 'LIVE' : 'SOON' }}
          </span>
        </div>
        <p class="text-[0.875rem] leading-[1.7] text-brand-muted">{{ a.desc }}</p>
      </li>
    </ul>

    <div class="rounded-[1.5rem] bg-white p-[1.5rem] shadow-card">
      <div class="mb-[1rem] flex items-center justify-between">
        <h2 class="text-[1.125rem] font-bold">試一下</h2>
        <button
          v-if="messages.length"
          class="text-[0.8125rem] text-brand-muted hover:underline"
          @click="clear"
        >
          清除
        </button>
      </div>

      <div
        class="mb-[1rem] flex max-h-[20rem] min-h-[8rem] flex-col gap-[0.5rem] overflow-y-auto rounded-[0.75rem] bg-brand-page p-[1rem]"
      >
        <p v-if="!messages.length" class="text-center text-[0.875rem] text-brand-muted">
          輸入訊息開始對話。提示:用 <code>/echo</code> 或 <code>/adk</code> 切換 Agent。
        </p>
        <div
          v-for="(m, i) in messages"
          :key="i"
          :class="m.role === 'user' ? 'self-end text-right' : 'self-start text-left'"
        >
          <div
            class="inline-block max-w-[80%] rounded-[0.75rem] px-[0.875rem] py-[0.5rem] text-[0.9375rem]"
            :class="m.role === 'user' ? 'bg-brand-ink text-white' : 'bg-white shadow-card'"
          >
            <span v-if="m.role === 'agent'" class="mr-[0.375rem] text-[0.6875rem] text-brand-muted"
              >[{{ m.agent }}]</span
            >
            {{ m.text }}
          </div>
        </div>
      </div>

      <form class="flex gap-[0.5rem]" @submit.prevent="onSend">
        <input
          v-model="input"
          type="text"
          placeholder="輸入訊息…"
          class="flex-1 rounded-full border border-brand-ink/15 px-[1rem] py-[0.5rem] text-[0.9375rem] outline-none focus:border-brand-start"
          :disabled="pending"
        />
        <button
          type="submit"
          :disabled="pending || !input.trim()"
          class="rounded-full bg-brand-ink px-[1.25rem] py-[0.5rem] text-[0.875rem] text-white disabled:opacity-50"
        >
          {{ pending ? '送出中…' : '送出' }}
        </button>
      </form>
      <p v-if="error" class="mt-[0.5rem] text-[0.8125rem] text-red-600">{{ error }}</p>
    </div>
  </section>
</template>
