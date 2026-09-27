import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/pages/HomePage.vue'),
    meta: { title: '首頁' },
  },
  {
    path: '/resume',
    name: 'resume',
    component: () => import('@/pages/ResumePage.vue'),
    meta: { title: '履歷' },
  },
  {
    path: '/resume/ats',
    name: 'resume-ats',
    component: () => import('@/pages/AtsResumePage.vue'),
    meta: { title: '履歷 ATS 版' },
  },
  {
    path: '/projects',
    name: 'projects',
    component: () => import('@/pages/ProjectsPage.vue'),
    meta: { title: '專案' },
  },
  {
    path: '/agents',
    name: 'agents',
    component: () => import('@/pages/AgentsPage.vue'),
    meta: { title: 'AI Agents' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/pages/NotFoundPage.vue'),
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to) {
    if (to.hash) return { el: to.hash, top: 80 }
    return { top: 0 }
  },
})

router.afterEach((to) => {
  const baseTitle = '廖啓舜 | Portfolio'
  const pageTitle = (to.meta?.title as string | undefined) ?? ''
  document.title = pageTitle ? `${pageTitle} · ${baseTitle}` : baseTitle
})
