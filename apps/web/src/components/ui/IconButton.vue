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
    class="inline-flex items-center gap-[0.5rem] rounded-full px-[1.125rem] py-[0.5rem] text-[0.875rem] font-medium transition disabled:cursor-not-allowed disabled:opacity-50"
    :class="
      variant === 'ghost'
        ? 'border border-brand-ink/15 bg-white text-brand-ink hover:bg-brand-sidebar'
        : 'bg-brand-ink text-white shadow-card hover:bg-brand-ink/90'
    "
    @click="$emit('click')"
  >
    <slot name="icon" />
    <span>{{ label }}</span>
  </button>
</template>
