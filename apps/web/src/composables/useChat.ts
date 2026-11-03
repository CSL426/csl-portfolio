import { ref } from 'vue'

export interface ChatMessage {
  role: 'user' | 'agent'
  text: string
  agent?: string
}

interface ChatResponse {
  agent: string
  text: string
  extra: Record<string, unknown>
}

export function useChat(defaultAgent?: string) {
  const messages = ref<ChatMessage[]>([])
  const pending = ref(false)
  const error = ref<string | null>(null)

  async function send(message: string): Promise<void> {
    const trimmed = message.trim()
    if (!trimmed) return
    messages.value.push({ role: 'user', text: trimmed })
    pending.value = true
    error.value = null
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ message: trimmed, agent: defaultAgent }),
      })
      if (res.status === 429) {
        throw new Error('訊息太頻繁，請稍後再試。')
      }
      if (!res.ok) {
        const body = await res.text()
        throw new Error(`API ${res.status}: ${body}`)
      }
      const data = (await res.json()) as ChatResponse
      messages.value.push({ role: 'agent', text: data.text, agent: data.agent })
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'unknown error'
    } finally {
      pending.value = false
    }
  }

  // The conversation lives on the server, so clearing only the list would let
  // the next reply keep using context the visitor can no longer see.
  async function clear(): Promise<void> {
    messages.value = []
    error.value = null
    try {
      const res = await fetch('/api/chat/session', { method: 'DELETE' })
      if (!res.ok) throw new Error(`API ${res.status}`)
    } catch {
      error.value = '無法清除伺服器上的對話，請稍後再試。'
    }
  }

  return { messages, pending, error, send, clear }
}
