import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('./pages/Login.vue'),
  },
  {
    path: '/',
    name: 'POS',
    component: () => import('./pages/POS.vue'),
  },
]

const router = createRouter({
  history: createWebHistory('/frontend'),
  routes,
})

export default router