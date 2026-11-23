<script setup lang="ts">
defineProps<{
  label: string
  disabled?: boolean
  variant?: 'primary' | 'ghost'
}>()

defineEmits<{ click: [] }>()
</script>

<template>
  <button
    type="button"
    :disabled="disabled"
    class="inline-flex items-center gap-[0.5rem] whitespace-nowrap rounded-full px-[1.125rem] py-[0.5rem] text-[0.875rem] font-medium transition-colors duration-[180ms] ease-[var(--ease-out)] active:translate-y-px disabled:cursor-not-allowed disabled:opacity-50 disabled:active:translate-y-0"
    :class="
      variant === 'ghost'
        ? 'border border-rule-strong bg-paper-2 text-ink hover:bg-surface-subtle'
        : 'bg-ink text-on-ink hover:bg-ink-hover'
    "
    @click="$emit('click')"
  >
    <slot name="icon" />
    <span>{{ label }}</span>
  </button>
</template>
