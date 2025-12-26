import { createRouter, createWebHistory } from 'vue-router'
import { session } from './data/session' // We will make this tiny helper next

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('./pages/Login.vue'),
  },
  {
    path: '/pos',
    name: 'POS',
    component: () => import('./pages/POS.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/',
    redirect: '/pos'
  }
]

const router = createRouter({
  history: createWebHistory('/frontend'),
  routes,
})

// Navigation Guard (The Bouncer)
router.beforeEach(async (to, from, next) => {
  const isLoggedIn = session.isLoggedIn;
  
  if (to.meta.requiresAuth && !isLoggedIn) {
    // 1. Try to fetch user (maybe they just refreshed the page)
    try {
      await session.fetch();
      if (session.isLoggedIn) {
        next();
      } else {
        next('/login');
      }
    } catch (e) {
      next('/login');
    }
  } else {
    next();
  }
})

export default router