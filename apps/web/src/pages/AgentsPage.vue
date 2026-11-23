<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'
import { useChat } from '@/composables/useChat'

interface AgentPreview {
  name: string
  desc: string
  status: 'coming-soon' | 'live'
}

const agents: AgentPreview[] = [
  {
    name: 'Claude',
    desc: 'Anthropic Claude Haiku 5.5，回覆快，適合公開聊天。',
    status: 'live',
  },
  {
    name: 'Gemini',
    desc: 'Google Gemini 3.5 Flash-Lite，輕量快速的對話模型。',
    status: 'coming-soon',
  },
  { name: 'Echo', desc: 'Pipeline 測試，把訊息回傳給你。', status: 'live' },
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

const pillButton =
  'shrink-0 whitespace-nowrap rounded-full transition-colors duration-[180ms] ease-[var(--ease-out)] active:translate-y-px'
</script>

<template>
  <section class="mx-auto max-w-[64rem] px-[1.25rem] pb-[2rem] pt-[3.5rem]">
    <header>
      <h1 class="font-display text-[clamp(2rem,4vw+0.5rem,3rem)] font-bold tracking-[-0.02em]">
        我正在打造的 AI 助手
      </h1>
      <p class="mt-[0.5rem] max-w-[40rem] text-[0.9375rem] leading-[1.8] text-ink-2">
        後端走 FastAPI，前端透過 <code>/api/chat</code> 呼叫，LINE bot 共用同一個 Agent 路由。
      </p>
    </header>

    <!-- One ruled strip instead of three shadowed cards. -->
    <ul
      class="mt-[2rem] grid divide-y divide-rule rounded-[var(--radius-card)] border border-rule bg-paper-2 sm:grid-cols-3 sm:divide-x sm:divide-y-0"
    >
      <li v-for="a in agents" :key="a.name" class="min-w-0 p-[1.25rem]">
        <div class="flex items-center justify-between gap-[0.75rem]">
          <h2 class="font-display text-[1.125rem] font-bold">{{ a.name }}</h2>
          <span
            class="rounded-full px-[0.5rem] py-[0.0625rem] font-mono text-[0.6875rem] font-medium"
            :class="
              a.status === 'live'
                ? 'bg-status-live-bg text-status-live-fg'
                : 'bg-status-soon-bg text-status-soon-fg'
            "
          >
            {{ a.status === 'live' ? 'LIVE' : 'SOON' }}
          </span>
        </div>
        <p class="mt-[0.5rem] text-[0.875rem] leading-[1.7] text-ink-2">{{ a.desc }}</p>
      </li>
    </ul>

    <!-- Workbench: a single flat surface, no card-in-card. -->
    <div class="mt-[2rem] rounded-[var(--radius-card)] border border-rule bg-paper-2">
      <div class="flex items-center justify-between gap-[1rem] border-b border-rule px-[1.25rem] py-[0.875rem]">
        <h2 class="font-display text-[1.125rem] font-bold">試一下</h2>
        <button
          v-if="messages.length"
          type="button"
          class="rounded-[var(--radius-control)] px-[0.375rem] text-[0.8125rem] text-ink-2 underline-offset-4 transition-colors duration-[180ms] ease-[var(--ease-out)] hover:text-ink hover:underline"
          @click="clear"
        >
          清除
        </button>
      </div>

      <div
        ref="messageList"
        class="flex max-h-[24rem] min-h-[10rem] flex-col gap-[0.625rem] overflow-y-auto px-[1.25rem] py-[1.25rem]"
      >
        <template v-if="!messages.length">
          <p class="text-[0.875rem] leading-[1.7] text-ink-2">
            輸入訊息開始對話，或點下面的問題。用 <code>/claude</code> 或 <code>/echo</code> 開頭可以切換 Agent。
          </p>
          <div class="flex flex-wrap gap-[0.5rem]">
            <button
              v-for="question in quickQuestions"
              :key="question"
              type="button"
              class="border border-rule-strong bg-paper-2 px-[0.875rem] py-[0.375rem] text-[0.8125rem] text-ink hover:bg-surface-subtle"
              :class="pillButton"
              @click="onQuickQuestion(question)"
            >
              {{ question }}
            </button>
          </div>
        </template>
        <div
          v-for="(m, i) in messages"
          :key="i"
          class="max-w-[85%]"
          :class="m.role === 'user' ? 'self-end' : 'self-start'"
        >
          <div
            class="rounded-[var(--radius-card)] px-[0.875rem] py-[0.5rem] text-[0.9375rem] leading-[1.7]"
            :class="m.role === 'user' ? 'bg-brand-ink text-white' : 'border border-rule bg-surface-subtle'"
          >
            <span v-if="m.role === 'agent'" class="mb-[0.125rem] block font-mono text-[0.6875rem] text-ink-2">
              {{ m.agent }}
            </span>
            <span class="whitespace-pre-wrap break-words">{{ m.text }}</span>
          </div>
        </div>
      </div>

      <form class="flex gap-[0.5rem] border-t border-rule px-[1.25rem] py-[0.875rem]" @submit.prevent="onSend">
        <input
          ref="inputField"
          v-model="input"
          type="text"
          placeholder="輸入訊息…"
          aria-label="輸入訊息"
          class="min-w-0 flex-1 rounded-full border border-rule-strong bg-paper px-[1rem] py-[0.5rem] text-[0.9375rem] text-ink placeholder:text-ink-2 focus-visible:border-focus"
        />
        <button
          type="submit"
          :disabled="pending || !input.trim()"
          class="bg-ink px-[1.25rem] py-[0.5rem] text-[0.875rem] font-medium text-on-ink hover:bg-ink-hover disabled:cursor-not-allowed disabled:opacity-50 disabled:active:translate-y-0"
          :class="pillButton"
        >
          {{ pending ? '送出中…' : '送出' }}
        </button>
      </form>
    </div>
    <p v-if="error" class="mt-[0.75rem] text-[0.8125rem] text-danger" role="alert">{{ error }}</p>
  </section>
</template>
