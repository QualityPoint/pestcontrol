import path from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import frappeui from 'frappe-ui/vite';
import proxyOptions from './proxyOptions';

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		frappeui({
			// We manage the proxy ourselves in proxyOptions.ts
			// (it injects X-Frappe-Site-Name: site.local which frappeProxy doesn't do)
			frappeProxy: false,
			lucideIcons: true,
			frappeTypes: false,
			jinjaBootData: true,
			buildConfig: {
				// Automatically detected outDir: ../pestcontrol/public/frontend
				// Automatically detected base: /assets/pestcontrol/frontend/
				indexHtmlPath: '../pestcontrol/www/pestcontrol.html',
			},
		}),
		vue(),
	],
	server: {
		port: 8080,
		host: '0.0.0.0',
		proxy: proxyOptions,
	},
	resolve: {
		alias: {
			'@': path.resolve(__dirname, 'src'),
		},
	},
	optimizeDeps: {
		include: ['feather-icons', 'interactjs'],
	},
});
