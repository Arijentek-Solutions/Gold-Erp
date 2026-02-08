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
  {
    path: '/catalogues',
    name: 'Catalogues',
    component: () => import('./pages/CatalogueDashboard.vue'),
  },
  {
    path: '/catalogues/:category',
    name: 'CategoryListing',
    component: () => import('./pages/CategoryListing.vue'),
  },
]

const router = createRouter({
  history: createWebHistory('/frontend'),
  routes,
})

export default router
