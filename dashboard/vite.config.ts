import path from 'path';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import proxyOptions from './proxyOptions';

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [react()],
	server: {
		port: 8080,
		host: '0.0.0.0',
		proxy: proxyOptions
	},
	resolve: {
		alias: {
			'@': path.resolve(__dirname, 'src')
		}
	},
	build: {
		outDir: '../pestcontrol/public/dashboard',
		emptyOutDir: true,
		target: 'es2015',
		// No manualChunks: splitting @mui/@emotion from react into separate
		// chunks produced a genuine circular chunk dependency (vendor-mui <->
		// vendor-react), which crashed at runtime with a TDZ ReferenceError
		// ("Cannot access '...' before initialization") — Rollup's default
		// chunking avoids this.
		rollupOptions: {
			output: {
				// Fixed (non-hashed) filenames: this bundle is now referenced by
				// three hand-written Jinja templates (portal.html, order.html,
				// me.html) instead of one generated index.html, so there's no
				// single place left to auto-sync a hash into. Cache-busting
				// instead goes through the site's existing asset_version() Jinja
				// helper (mtime-based query param), same as custom.css/skystar.css.
				entryFileNames: 'assets/main.js',
				chunkFileNames: 'assets/[name].js',
				assetFileNames: 'assets/[name][extname]'
			}
		}
	}
});
