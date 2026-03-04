import type { RouteRecordRaw } from 'vue-router';

const authRoutes: RouteRecordRaw[] = [
	{
		path: '/login',
		name: 'Login',
		component: () => import('../views/Login.vue'),
		meta: {
			isLoginPage: true
		},
		props: true
	}
];

export default authRoutes;
