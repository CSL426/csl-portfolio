<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { resumeData } from '@/data/resume'
import IconButton from '@/components/ui/IconButton.vue'

function handlePrint() {
  window.print()
}
</script>

<template>
  <div class="flex flex-col items-center gap-[1.125rem] px-[1rem] py-[1.5rem] print:gap-0 print:p-0">
    <!-- Toolbar -->
    <div
      class="no-print sticky top-[3.5rem] z-20 flex w-full max-w-[52rem] flex-wrap items-center justify-between gap-[0.75rem] rounded-[1rem] bg-white/85 px-[1.25rem] py-[0.75rem] shadow-card backdrop-blur"
    >
      <div>
        <p class="text-[0.75rem] tracking-[0.2em] text-brand-muted">ATS RESUME</p>
        <h2 class="text-[1.125rem] font-bold">廖啓舜 · ATS 純文字版</h2>
      </div>
      <div class="flex flex-wrap items-center gap-[0.5rem]">
        <IconButton label="列印 / 另存 PDF" @click="handlePrint" />
        <RouterLink
          to="/resume"
          class="inline-flex items-center rounded-full border border-brand-ink/15 bg-white px-[1.125rem] py-[0.5rem] text-[0.875rem] font-medium text-brand-ink transition hover:bg-brand-sidebar"
        >
          回視覺版
        </RouterLink>
      </div>
    </div>
    <p class="no-print w-full max-w-[52rem] text-[0.8125rem] leading-[1.7] text-brand-muted">
      此版本為 ATS(求職系統自動篩選)友善格式:單欄、純文字、無照片與圖示。請用「列印 /
      另存 PDF」輸出,文字可被系統正確解析;勿使用視覺版的圖片式 PDF 上傳求職平台。
    </p>

    <!-- ATS document -->
    <article class="ats-page">
      <header>
        <h1 class="text-[1.5rem] font-bold">
          {{ resumeData.profile.nameZh }} {{ resumeData.profile.nameEn }}
        </h1>
        <p class="mt-[0.375rem]">
          <template v-for="(contact, idx) in resumeData.profile.contacts" :key="contact.label">
            <span v-if="idx > 0"> | </span>
            <span>{{ contact.label }}: {{ contact.value }}</span>
          </template>
        </p>
      </header>

      <section>
        <h2 class="ats-heading">專長摘要 Summary</h2>
        <ul class="ats-list">
          <li v-for="strength in resumeData.strengths" :key="strength">{{ strength }}</li>
        </ul>
      </section>

      <section>
        <h2 class="ats-heading">工作經歷 Work Experience</h2>
        <div v-for="experience in resumeData.experiences" :key="experience.title" class="ats-entry">
          <h3 class="font-bold">{{ experience.title }}</h3>
          <ul class="ats-list">
            <li v-for="bullet in experience.bullets" :key="bullet">{{ bullet }}</li>
          </ul>
        </div>
      </section>

      <section>
        <h2 class="ats-heading">學歷 Education</h2>
        <div v-for="item in resumeData.education" :key="item.degree" class="ats-entry">
          <p class="font-bold">{{ item.school }} {{ item.degree }}({{ item.period }})</p>
          <p v-if="item.note">論文主題:{{ item.note }}</p>
        </div>
      </section>

      <section>
        <h2 class="ats-heading">技能 Skills</h2>
        <p>{{ resumeData.tools.join('、') }}</p>
      </section>

      <section>
        <h2 class="ats-heading">推薦人 Reference</h2>
        <p>
          {{ resumeData.reference.name }}({{ resumeData.reference.role }})| Email:
          {{ resumeData.reference.email }} | Phone: {{ resumeData.reference.phone }}
        </p>
      </section>
    </article>
  </div>
</template>

<style>
.ats-page {
  width: 210mm;
  max-width: 100%;
  background: #fff;
  color: #111;
  box-shadow: 0 1.25rem 2.8125rem rgba(0, 0, 0, 0.18);
  border-radius: 0.75rem;
  padding: 18mm 20mm;
  font-size: 0.8125rem;
  line-height: 1.8;
}
.ats-page section {
  margin-top: 1.25rem;
}
.ats-page p {
  margin-top: 0.375rem;
}
.ats-heading {
  font-size: 1rem;
  font-weight: 700;
  border-bottom: 1px solid #111;
  padding-bottom: 0.25rem;
}
.ats-entry {
  margin-top: 0.75rem;
}
.ats-list {
  list-style: disc;
  padding-left: 1.25rem;
  margin-top: 0.375rem;
}

@media print {
  @page ats {
    size: A4;
    margin: 10mm 15mm;
  }
  .ats-page {
    page: ats;
    box-shadow: none !important;
    border-radius: 0 !important;
    width: 100% !important;
    padding: 0 !important;
    font-size: 0.75rem !important;
    line-height: 1.45 !important;
  }
  .ats-page section {
    margin-top: 0.875rem !important;
    break-inside: avoid-page;
  }
  .ats-heading {
    font-size: 0.9375rem !important;
    padding-bottom: 0.125rem !important;
  }
  .ats-entry {
    margin-top: 0.4rem !important;
  }
  .ats-list {
    margin-top: 0.2rem !important;
    padding-left: 1rem !important;
  }
}
</style>
