<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'
import { useChat } from '@/composables/useChat'

interface AgentPreview {
  name: string
  desc: string
  status: 'coming-soon' | 'live'
}

const agents: AgentPreview[] = [
  { name: 'Echo', desc: 'Pipeline 測試，把訊息回傳給你。', status: 'live' },
  {
    name: 'Gemini',
    desc: 'Google Gemini 3.5 Flash-Lite，輕量快速的對話模型。',
    status: 'live',
  },
  {
    name: 'Claude',
    desc: 'Anthropic Claude Haiku 5.5，回覆快，適合公開聊天。',
    status: 'live',
  },
]

const quickQuestions = ['他的技術專長是什麼？', '他做過哪些專案？', 'ai-config 是什麼？', '怎麼聯絡他？']

const input = ref('')
const inputField = ref<HTMLInputElement | null>(null)
const { messages, pending, error, send, clear } = useChat()

const messageList = ref<HTMLElement | null>(null)

watch(
  () => messages.value.length,
  async () => {
    await nextTick()
    if (messageList.value) messageList.value.scrollTop = messageList.value.scrollHeight
  },
)

async function onQuickQuestion(question: string) {
  if (pending.value) return
  // The button disappears once the chat starts. Refocus so the visitor can keep
  // typing, but not on touch screens, where it would open the keyboard over the reply.
  if (window.matchMedia('(pointer: fine)').matches) inputField.value?.focus()
  await send(question)
}

async function onSend() {
  // The field stays enabled so it keeps focus; a disabled input loses it, and
  // visitors had to click back in after every message.
  if (pending.value || !input.value.trim()) return
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
        後端走 FastAPI，前端透過 <code>/api/chat</code> 呼叫，LINE bot 共用同一個 Agent 路由。
      </p>
    </div>

    <ul class="mb-[2.5rem] grid gap-[1.25rem] sm:grid-cols-2 lg:grid-cols-3">
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
        ref="messageList"
        class="mb-[1rem] flex max-h-[20rem] min-h-[8rem] flex-col gap-[0.5rem] overflow-y-auto rounded-[0.75rem] bg-brand-page p-[1rem]"
      >
        <template v-if="!messages.length">
          <p class="text-center text-[0.875rem] text-brand-muted">
            輸入訊息開始對話。提示：用 <code>/claude</code>、<code>/gemini</code> 或 <code>/echo</code> 開頭切換 Agent。
          </p>
          <div class="mt-[0.75rem] flex flex-wrap justify-center gap-[0.5rem]">
            <button
              v-for="question in quickQuestions"
              :key="question"
              type="button"
              class="rounded-full border border-brand-ink/15 bg-white px-[0.875rem] py-[0.375rem] text-[0.8125rem] text-brand-ink transition hover:bg-brand-sidebar"
              @click="onQuickQuestion(question)"
            >
              {{ question }}
            </button>
          </div>
        </template>
        <div
          v-for="(m, i) in messages"
          :key="i"
          class="max-w-[80%]"
          :class="m.role === 'user' ? 'self-end' : 'self-start'"
        >
          <div
            class="rounded-[0.75rem] px-[0.875rem] py-[0.5rem] text-[0.9375rem]"
            :class="m.role === 'user' ? 'bg-brand-ink text-white' : 'bg-white shadow-card'"
          >
            <span v-if="m.role === 'agent'" class="mr-[0.375rem] text-[0.6875rem] text-brand-muted"
              >[{{ m.agent }}]</span
            >
            <span class="whitespace-pre-wrap break-words">{{ m.text }}</span>
          </div>
        </div>
      </div>

      <form class="flex gap-[0.5rem]" @submit.prevent="onSend">
        <input
          ref="inputField"
          v-model="input"
          type="text"
          placeholder="輸入訊息…"
          class="min-w-0 flex-1 rounded-full border border-brand-ink/15 px-[1rem] py-[0.5rem] text-[0.9375rem] outline-none focus:border-brand-start"
        />
        <button
          type="submit"
          :disabled="pending || !input.trim()"
          class="shrink-0 whitespace-nowrap rounded-full bg-brand-ink px-[1.25rem] py-[0.5rem] text-[0.875rem] text-white disabled:opacity-50"
        >
          {{ pending ? '送出中…' : '送出' }}
        </button>
      </form>
      <p v-if="error" class="mt-[0.5rem] text-[0.8125rem] text-red-600">{{ error }}</p>
    </div>
  </section>
</template>
