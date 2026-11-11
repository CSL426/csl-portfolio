import { expect, test, type Page } from '@playwright/test'

// /api/chat is mocked so timing is controlled and no model is called.
interface ChatMock {
  posts: { message: string }[]
  deletes: number
  statuses: number[]
  delayMs: number
}

async function mockChat(page: Page): Promise<ChatMock> {
  const mock: ChatMock = { posts: [], deletes: 0, statuses: [], delayMs: 300 }
  await page.route('**/api/chat/session', async (route) => {
    mock.deletes += 1
    await route.fulfill({ status: 204 })
  })
  await page.route('**/api/chat', async (route) => {
    mock.posts.push(route.request().postDataJSON())
    await new Promise((resolve) => setTimeout(resolve, mock.delayMs))
    const status = mock.statuses.shift() ?? 200
    await route.fulfill({
      status,
      contentType: 'application/json',
      body: JSON.stringify(
        status === 200
          ? { agent: 'claude', text: `回覆 ${mock.posts.length}`, extra: {} }
          : { detail: 'error' },
      ),
    })
  })
  return mock
}

const chatInput = (page: Page) => page.getByPlaceholder('輸入訊息…')
const messageList = (page: Page) => page.locator('.overflow-y-auto')
const isFocused = (page: Page) =>
  chatInput(page).evaluate((el) => el === document.activeElement)

test.describe('chat', () => {
  test('keeps focus so messages can be sent with Enter only', async ({ page }) => {
    const mock = await mockChat(page)
    await page.goto('/agents')
    const input = chatInput(page)

    await input.click()
    await input.fill('第一則')
    await input.press('Enter')
    expect(await isFocused(page)).toBe(true)
    await expect(page.getByText('回覆 1')).toBeVisible()
    expect(await isFocused(page)).toBe(true)

    await page.keyboard.type('第二則')
    await page.keyboard.press('Enter')
    await expect(page.getByText('回覆 2')).toBeVisible()
    expect(mock.posts.map((p) => p.message)).toEqual(['第一則', '第二則'])
  })

  test('Enter while waiting neither double sends nor drops the draft', async ({ page }) => {
    const mock = await mockChat(page)
    await page.goto('/agents')
    const input = chatInput(page)

    await input.fill('送出中')
    await input.press('Enter')
    await input.fill('還沒送')
    await input.press('Enter')
    await expect(page.getByText('回覆 1')).toBeVisible()
    expect(mock.posts).toHaveLength(1)
    await expect(input).toHaveValue('還沒送')
  })

  test('empty Enter sends nothing', async ({ page }) => {
    const mock = await mockChat(page)
    await page.goto('/agents')
    await chatInput(page).press('Enter')
    await page.waitForTimeout(200)
    expect(mock.posts).toHaveLength(0)
  })

  test('scrolls to the newest message', async ({ page }) => {
    const mock = await mockChat(page)
    mock.delayMs = 10
    await page.goto('/agents')
    const input = chatInput(page)
    for (let i = 1; i <= 12; i += 1) {
      await input.fill(`捲動 ${i}`)
      await input.press('Enter')
      await expect(page.getByText(`回覆 ${i}`, { exact: true })).toBeVisible()
    }
    const scroll = await messageList(page).evaluate((el) => el.scrollHeight - el.scrollTop - el.clientHeight)
    expect(scroll).toBeLessThanOrEqual(4)
  })

  test('shows errors and keeps focus', async ({ page }) => {
    const mock = await mockChat(page)
    mock.statuses.push(429)
    await page.goto('/agents')
    await chatInput(page).fill('太快')
    await chatInput(page).press('Enter')
    await expect(page.getByText('訊息太頻繁')).toBeVisible()
    expect(await isFocused(page)).toBe(true)
  })

  test('Clear empties the list and the server session', async ({ page }) => {
    const mock = await mockChat(page)
    await page.goto('/agents')
    await chatInput(page).fill('hi')
    await chatInput(page).press('Enter')
    await expect(page.getByText('回覆 1')).toBeVisible()
    await page.getByRole('button', { name: '清除' }).click()
    await expect(page.getByText('回覆 1')).toHaveCount(0)
    expect(mock.deletes).toBe(1)
  })

  test('quick questions send and hand focus back to the input', async ({ page }) => {
    const mock = await mockChat(page)
    await page.goto('/agents')
    const quick = messageList(page).getByRole('button')
    await expect(quick).toHaveCount(4)
    const question = await quick.first().innerText()
    await quick.first().click()
    expect(await isFocused(page)).toBe(true)
    await expect(page.getByText('回覆 1')).toBeVisible()
    expect(mock.posts[0].message).toBe(question)
    await expect(quick).toHaveCount(0)
  })

  test('short messages stay on one line and long ones wrap inside the list', async ({ page }) => {
    await mockChat(page)
    await page.goto('/agents')
    const input = chatInput(page)
    const bubbles = messageList(page).locator('.bg-brand-ink')

    await input.fill('一段不算太長的使用者訊息應該要在同一行顯示')
    await input.press('Enter')
    await expect(page.getByText('回覆 1')).toBeVisible()
    expect((await bubbles.last().boundingBox())!.height).toBeLessThan(48)

    await input.fill('很長'.repeat(90))
    await input.press('Enter')
    await expect(page.getByText('回覆 2')).toBeVisible()
    const fits = await bubbles.last().evaluate((el) => {
      const list = el.closest('.overflow-y-auto')!
      return el.getBoundingClientRect().right <= list.getBoundingClientRect().right && list.scrollWidth <= list.clientWidth
    })
    expect(fits).toBe(true)
  })
})

test.describe('phone', () => {
  test.use({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })

  test('chat fits the screen and still sends', async ({ page }) => {
    const mock = await mockChat(page)
    await page.goto('/agents')
    const input = chatInput(page)
    await input.tap()
    await input.fill('手機')
    await input.press('Enter')
    await expect(page.getByText('回覆 1')).toBeVisible()
    expect(mock.posts).toHaveLength(1)

    const box = (await input.boundingBox())!
    expect(box.x + box.width).toBeLessThanOrEqual(390)
    // The Send button used to wrap onto two lines and stretch the row.
    expect(box.height).toBeLessThan(48)
  })

  for (const path of ['/', '/resume', '/resume/ats', '/projects', '/agents']) {
    test(`${path} has no sideways scroll`, async ({ page }) => {
      await page.goto(path)
      await page.waitForLoadState('networkidle')
      const [scrollWidth, clientWidth] = await page.evaluate(() => [
        document.documentElement.scrollWidth,
        document.documentElement.clientWidth,
      ])
      expect(scrollWidth).toBeLessThanOrEqual(clientWidth)
    })
  }
})

test.describe('navigation and downloads', () => {
  test('nav links and the not-found page work', async ({ page }) => {
    const errors: string[] = []
    page.on('pageerror', (error) => errors.push(error.message))
    await page.goto('/')
    for (const [label, path] of [
      ['Resume', '/resume'],
      ['Projects', '/projects'],
      ['Agents', '/agents'],
      ['Home', '/'],
    ]) {
      await page.locator('nav').getByRole('link', { name: label, exact: true }).click()
      await expect(page).toHaveURL(new RegExp(`${path === '/' ? '/$' : path}$`))
    }
    await page.goto('/no-such-page')
    await expect(page.getByText('404')).toBeVisible()
    expect(errors).toEqual([])
  })

  test('resume downloads and the ATS link work', async ({ page }) => {
    test.setTimeout(120_000)
    await page.goto('/resume')
    for (const name of ['官方版 PDF', '下載 PNG', '下載 PDF (現場輸出)']) {
      const download = page.waitForEvent('download', { timeout: 60_000 })
      await page.getByRole('button', { name }).click()
      expect(await (await download).path()).toBeTruthy()
    }
    await page.getByRole('link', { name: 'ATS 版' }).click()
    await expect(page).toHaveURL(/\/resume\/ats$/)
  })
})
