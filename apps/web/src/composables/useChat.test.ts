import { afterEach, describe, expect, it, vi } from 'vitest'
import { useChat } from './useChat'

function stubFetch(status: number, body: unknown = {}) {
  const fetchMock = vi.fn(async () => new Response(JSON.stringify(body), { status }))
  vi.stubGlobal('fetch', fetchMock)
  return fetchMock
}

describe('useChat', () => {
  afterEach(() => vi.unstubAllGlobals())

  it('does not send a client-chosen user id', async () => {
    const fetchMock = stubFetch(200, { agent: 'echo', text: 'hi', extra: {} })
    await useChat().send('hello')
    const init = (fetchMock.mock.calls[0] as unknown as [string, RequestInit])[1]
    expect(JSON.parse(init.body as string)).not.toHaveProperty('user_id')
  })

  it('shows a readable message when rate limited', async () => {
    stubFetch(429)
    const chat = useChat()
    await chat.send('hello')
    expect(chat.error.value).toBe('訊息太頻繁，請稍後再試。')
  })

  it('clears the server-side conversation too', async () => {
    const fetchMock = vi.fn(async () => new Response(null, { status: 204 }))
    vi.stubGlobal('fetch', fetchMock)
    await useChat().clear()
    expect(fetchMock).toHaveBeenCalledWith('/api/chat/session', { method: 'DELETE' })
  })

  it('reports when the server-side conversation could not be cleared', async () => {
    stubFetch(500)
    const chat = useChat()
    await chat.clear()
    expect(chat.error.value).toContain('無法清除')
  })
})
