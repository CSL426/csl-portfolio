import { onBeforeUnmount, onMounted, ref } from 'vue'

/** A4 width in CSS pixels (210 mm at 96 dpi). */
export const A4_WIDTH_PX = (210 * 96) / 25.4

/**
 * Scale factor that fits a fixed-width sheet inside the viewport, capped at 1.
 * The resume pages are laid out at A4 size for print and PDF export; on a
 * phone they would otherwise force horizontal scrolling.
 */
export function useFitScale(sheetWidthPx = A4_WIDTH_PX, gutterPx = 32) {
  const scale = ref(1)

  function update() {
    if (typeof window === 'undefined') return
    scale.value = Math.min(1, (window.innerWidth - gutterPx) / sheetWidthPx)
  }

  onMounted(() => {
    update()
    window.addEventListener('resize', update, { passive: true })
  })
  onBeforeUnmount(() => window.removeEventListener('resize', update))

  return { scale, update }
}
