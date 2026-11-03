<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { A4_WIDTH_PX } from '@/composables/useFitScale'

/**
 * Wraps one A4 `.resume-page` and shrinks it with a CSS transform so the
 * whole sheet stays visible on narrow screens. The wrapper reserves the
 * scaled height so following pages flow normally. Print and export use the
 * unscaled sheet: print via the stylesheet, export by passing `scale = 1`.
 */
const props = defineProps<{ scale: number }>()

const sheet = ref<HTMLElement | null>(null)
const sheetHeight = ref(0)
let observer: ResizeObserver | null = null

onMounted(() => {
  if (!sheet.value) return
  sheetHeight.value = sheet.value.offsetHeight
  observer = new ResizeObserver(() => {
    if (sheet.value) sheetHeight.value = sheet.value.offsetHeight
  })
  observer.observe(sheet.value)
})
onBeforeUnmount(() => observer?.disconnect())

const wrapperStyle = computed(() => ({
  width: `${A4_WIDTH_PX * props.scale}px`,
  height: sheetHeight.value ? `${sheetHeight.value * props.scale}px` : undefined,
}))
const sheetStyle = computed(() => ({
  transform: props.scale === 1 ? undefined : `scale(${props.scale})`,
  transformOrigin: 'top left',
}))

defineExpose({ sheet })
</script>

<template>
  <div class="resume-sheet-wrapper" :style="wrapperStyle">
    <section ref="sheet" class="resume-page resume-sheet" :style="sheetStyle">
      <slot />
    </section>
  </div>
</template>
