import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import Home from '../views/Home.vue';
import authRoutes from './auth';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  ...authRoutes,
];

const router = createRouter({
  history: createWebHistory('/frontend'),
  routes,
});

export default router;
