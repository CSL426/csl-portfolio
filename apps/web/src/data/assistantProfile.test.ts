import { expect, it } from 'vitest'
import { projects } from '@/data/projects'
import { resumeData } from '@/data/resume'

// The API gives this file to the chat assistant, so its answers come from the
// same copy the site shows. A stale file fails here; `pnpm update:profile` rewrites it.
// The reference is left out: a chatbot should not hand a third party's phone number
// to anyone who asks.
const profile = `${JSON.stringify(
  { resume: { ...resumeData, reference: undefined }, projects },
  null,
  2,
)}\n`

it('keeps the assistant profile in sync with the site copy', async () => {
  await expect(profile).toMatchFileSnapshot('../../../api/server/core/site_profile.json')
})

it('does not give the assistant the contact details of the reference', () => {
  const { name, email, phone } = resumeData.reference
  for (const detail of [name, email, phone]) {
    expect(profile).not.toContain(detail)
  }
})
