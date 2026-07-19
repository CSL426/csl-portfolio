<script setup lang="ts">
import { ref } from 'vue'
import { resumeData } from '@/data/resume'
import { useDownload } from '@/composables/useDownload'
import ProfileCard from '@/components/resume/ProfileCard.vue'
import SidebarPanel from '@/components/resume/SidebarPanel.vue'
import ExperienceCard from '@/components/resume/ExperienceCard.vue'
import AutobioCard from '@/components/resume/AutobioCard.vue'
import EnglishSection from '@/components/resume/EnglishSection.vue'
import IconButton from '@/components/ui/IconButton.vue'

const mainExperiences = resumeData.experiences.filter(
  (exp) => !exp.title.startsWith('學術研究'),
)
const academicExperiences = resumeData.experiences.filter((exp) =>
  exp.title.startsWith('學術研究'),
)

const page1 = ref<HTMLElement | null>(null)
const page2 = ref<HTMLElement | null>(null)
const page3 = ref<HTMLElement | null>(null)

const { isExporting, error, exportPng, exportPdf, downloadAsset } = useDownload()

function getPageNodes(): HTMLElement[] {
  return [page1.value, page2.value, page3.value].filter((el): el is HTMLElement => el !== null)
}

function handlePng() {
  void exportPng(getPageNodes(), '廖啓舜_履歷')
}

function handlePdf() {
  void exportPdf(getPageNodes(), '廖啓舜_履歷')
}

function handleOfficialPdf() {
  const filename = '廖啓舜_履歷.pdf'
  downloadAsset(`/${encodeURIComponent(filename)}`, filename)
}
</script>

<template>
  <div class="flex flex-col items-center gap-[1.125rem] px-[1rem] py-[1.5rem] print:gap-0 print:p-0">
    <!-- Toolbar -->
    <div
      class="no-print sticky top-[3.5rem] z-20 flex w-full max-w-[52rem] flex-wrap items-center justify-between gap-[0.75rem] rounded-[1rem] bg-white/85 px-[1.25rem] py-[0.75rem] shadow-card backdrop-blur"
    >
      <div>
        <p class="text-[0.75rem] tracking-[0.2em] text-brand-muted">RESUME</p>
        <h2 class="text-[1.125rem] font-bold">廖啓舜 · Liao Chi-Shun</h2>
      </div>
      <div class="flex flex-wrap items-center gap-[0.5rem]">
        <IconButton
          label="下載 PDF (現場輸出)"
          :disabled="isExporting"
          @click="handlePdf"
        />
        <IconButton
          label="下載 PNG"
          variant="ghost"
          :disabled="isExporting"
          @click="handlePng"
        />
        <IconButton
          label="官方版 PDF"
          variant="ghost"
          @click="handleOfficialPdf"
        />
        <RouterLink
          to="/resume/ats"
          class="inline-flex items-center rounded-full border border-brand-ink/15 bg-white px-[1.125rem] py-[0.5rem] text-[0.875rem] font-medium text-brand-ink transition hover:bg-brand-sidebar"
        >
          ATS 版
        </RouterLink>
      </div>
    </div>
    <p v-if="error" class="no-print text-[0.875rem] text-red-600">{{ error }}</p>
    <p v-if="isExporting" class="no-print text-[0.875rem] text-brand-muted">輸出中…</p>

    <!-- Page 1 -->
    <section ref="page1" class="resume-page">
      <span
        class="absolute right-[22mm] bottom-[18mm] text-[0.6875rem] tracking-[0.12em] text-brand-ink/45"
        >01</span
      >
      <div class="resume-frame">
        <ProfileCard :profile="resumeData.profile" />
        <div class="mt-[0.75rem]">
          <ExperienceCard :strengths="resumeData.strengths" />
        </div>
        <div class="mt-[0.75rem] grid grid-cols-[30%_70%] gap-[1rem]">
          <SidebarPanel :education="resumeData.education" :academic="academicExperiences" />
          <ExperienceCard :experiences="mainExperiences" />
        </div>
        <p
          class="mx-auto mt-[0.25rem] text-center text-[0.75rem] leading-[1.5] text-brand-muted"
        >
          推薦人:{{ resumeData.reference.name }} {{ resumeData.reference.role }}｜{{
            resumeData.reference.email
          }}｜{{ resumeData.reference.phone }}
        </p>
      </div>
    </section>

    <!-- Page 2 -->
    <section ref="page2" class="resume-page">
      <span
        class="absolute right-[22mm] bottom-[18mm] text-[0.6875rem] tracking-[0.12em] text-brand-ink/45"
        >02</span
      >
      <div class="resume-frame flex flex-col gap-[1.625rem]">
        <AutobioCard :sections="resumeData.autobiography" />
      </div>
    </section>

    <!-- Page 3 -->
    <section ref="page3" class="resume-page">
      <span
        class="absolute right-[22mm] bottom-[18mm] text-[0.6875rem] tracking-[0.12em] text-brand-ink/45"
        >03</span
      >
      <div class="resume-frame">
        <EnglishSection :sections="resumeData.english" />
      </div>
    </section>
  </div>
</template>
