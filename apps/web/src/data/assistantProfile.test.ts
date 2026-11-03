import { expect, it } from 'vitest'
import { projects } from '@/data/projects'
import { resumeData } from '@/data/resume'

// The API gives this file to the chat assistant, so its answers come from the
// same copy the site shows. A stale file fails here; `pnpm update:profile` rewrites it.
it('keeps the assistant profile in sync with the site copy', async () => {
  const profile = `${JSON.stringify({ resume: resumeData, projects }, null, 2)}\n`
  await expect(profile).toMatchFileSnapshot('../../../api/server/core/site_profile.json')
})
