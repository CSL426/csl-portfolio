import { afterEach, describe, expect, it, vi } from 'vitest'
import { A4_WIDTH_PX, useFitScale } from './useFitScale'

function stubViewport(layoutWidth: number, innerWidth: number) {
  vi.stubGlobal('document', { documentElement: { clientWidth: layoutWidth } })
  vi.stubGlobal('window', { innerWidth })
  // onMounted warns when the composable runs outside a component; only update() is under test.
  vi.spyOn(console, 'warn').mockImplementation(() => undefined)
}

describe('useFitScale', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
    vi.restoreAllMocks()
  })

  it('fits the layout viewport even when a phone reports a wider innerWidth', () => {
    // Mobile browsers grow innerWidth to fit overflowing content, which made the
    // sheet too large and cut off its left side.
    stubViewport(390, 794)
    const { scale, update } = useFitScale()
    update()
    expect(scale.value).toBeCloseTo((390 - 32) / A4_WIDTH_PX)
  })

  it('never scales above full size', () => {
    stubViewport(390, 390)
    const { scale, update } = useFitScale()
    update()
    expect(scale.value).toBeLessThan(1)

    stubViewport(1280, 1280)
    update()
    expect(scale.value).toBe(1)
  })
})
