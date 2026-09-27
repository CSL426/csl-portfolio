import { describe, expect, it } from 'vitest'
import { resumeData } from '@/data/resume'
import { projects } from '@/data/projects'

/**
 * Half-width `,` `;` `:` `(` `)` directly next to a CJK character. The site
 * copy uses full-width punctuation inside Chinese text (，；：（）); half-width
 * marks are still fine inside Latin runs such as "POC/MVP" or "React/Vue".
 */
const HALF_WIDTH_NEXT_TO_CJK = /[一-鿿][,;:()]|[,;:()][一-鿿]/u

function collectStrings(value: unknown, out: string[] = []): string[] {
  if (typeof value === 'string') out.push(value)
  else if (Array.isArray(value)) value.forEach((v) => collectStrings(v, out))
  else if (value && typeof value === 'object')
    Object.values(value).forEach((v) => collectStrings(v, out))
  return out
}

describe('resume data', () => {
  it('uses full-width punctuation inside Chinese copy', () => {
    const offenders = collectStrings({
      experiences: resumeData.experiences,
      strengths: resumeData.strengths,
      autobiography: resumeData.autobiography,
      education: resumeData.education,
    }).filter((s) => HALF_WIDTH_NEXT_TO_CJK.test(s))
    expect(offenders).toEqual([])
  })

  it('has a contact link for every contact', () => {
    for (const c of resumeData.profile.contacts) {
      expect(c.href, c.label).toMatch(/^(mailto:|tel:|https?:)/)
    }
  })

  it('keeps the visual resume within three pages of content', () => {
    // Page 1 is laid out by hand; a large jump in bullet count is the usual
    // reason it overflows A4. Bump this deliberately after re-measuring.
    const bullets = resumeData.experiences.reduce((n, e) => n + e.bullets.length, 0)
    expect(bullets).toBeLessThanOrEqual(10)
  })
})

describe('projects data', () => {
  it('has unique, URL-safe ids', () => {
    const ids = projects.map((p) => p.id)
    expect(new Set(ids).size).toBe(ids.length)
    for (const id of ids) expect(id).toMatch(/^[a-z0-9-]+$/)
  })

  it('features exactly one project', () => {
    expect(projects.filter((p) => p.featured)).toHaveLength(1)
  })

  it('only links to https URLs', () => {
    for (const p of projects) {
      for (const l of p.links ?? []) expect(l.href, `${p.id}:${l.label}`).toMatch(/^https:\/\//)
    }
  })

  it('uses full-width punctuation inside Chinese copy', () => {
    const offenders = collectStrings(
      projects.map(({ name, tagline, summary, highlights }) => ({ name, tagline, summary, highlights })),
    ).filter((s) => HALF_WIDTH_NEXT_TO_CJK.test(s))
    expect(offenders).toEqual([])
  })
})
