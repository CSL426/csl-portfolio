<script setup lang="ts">
import AppNav from '@/components/ui/AppNav.vue'
</script>

<template>
  <div class="flex min-h-screen flex-col">
    <AppNav class="no-print" />
    <main class="flex-1">
      <RouterView />
    </main>
    <footer class="no-print py-6 text-center text-xs text-brand-muted">
      © {{ new Date().getFullYear() }} 廖啓舜 · Spark
    </footer>
  </div>
</template>
