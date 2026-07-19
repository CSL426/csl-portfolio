<script setup lang="ts">
import type { ProfileInfo } from '@/types/resume'

defineProps<{ profile: ProfileInfo }>()
</script>

<template>
  <div
    class="grid grid-cols-[auto_1fr] items-start gap-[1.375rem] rounded-[1.75rem] px-[1.875rem] py-[1.25rem] shadow-profile"
    style="background: linear-gradient(135deg, #76abd6, #8ebfe5)"
  >
    <div
      class="h-[9.375rem] w-[9.375rem] overflow-hidden rounded-full border-[0.375rem] border-white/85"
      style="
        background: linear-gradient(135deg, #d9ebff, #bed6ef);
        box-shadow: 0 0 0 0.625rem rgba(255, 255, 255, 0.42);
      "
    >
      <img
        src="/profile.jpg"
        alt="廖啓舜 個人照"
        class="h-full w-full object-cover object-top"
      />
    </div>
    <div class="text-white">
      <h1 class="m-0 mb-[0.25rem] text-[1.875rem] tracking-[0.08em]">
        {{ profile.nameZh }}
      </h1>
      <span class="mb-[0.875rem] block text-[1rem] text-white/85">
        {{ profile.nameEn }}
      </span>
      <ul class="m-0 flex list-none flex-col gap-[0.375rem] p-0 text-[0.9375rem]">
        <li
          v-for="c in profile.contacts"
          :key="c.label"
          class="flex items-center gap-[0.5rem] text-white/95"
        >
          <span class="min-w-[3.375rem] font-semibold">{{ c.label }}</span>
          <a v-if="c.href" :href="c.href" class="hover:underline">{{ c.value }}</a>
          <span v-else>{{ c.value }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>
