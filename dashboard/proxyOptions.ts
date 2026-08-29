import { existsSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

// This is dev-server-only (used by `yarn dev`'s server.proxy), but the
// module is imported unconditionally by vite.config.ts, so it must never
// throw during a production build. The pestcontrol app's real source lives
// outside the bench tree and is reached through a symlink at
// <bench>/apps/pestcontrol — both import.meta.url and process.cwd() resolve
// through that symlink to the *real* path, so a fixed "../../../sites/..."
// offset (which works for apps that live directly under apps/, e.g.
// erpnext/banking) can't be assumed here. Search upward instead.
function findCommonSiteConfig(): string | undefined {
	const startPoints = [dirname(fileURLToPath(import.meta.url)), process.cwd()];
	for (const start of startPoints) {
		let dir = start;
		for (let i = 0; i < 8; i++) {
			const candidate = join(dir, 'sites', 'common_site_config.json');
			if (existsSync(candidate)) return candidate;
			const parent = dirname(dir);
			if (parent === dir) break;
			dir = parent;
		}
	}
	return undefined;
}

const DEFAULT_WEBSERVER_PORT = 8000;

function getWebserverPort(): number {
	const configPath = findCommonSiteConfig();
	if (!configPath) {
		console.warn(
			`[proxyOptions] Could not locate sites/common_site_config.json; falling back to port ${DEFAULT_WEBSERVER_PORT} for the dev proxy.`
		);
		return DEFAULT_WEBSERVER_PORT;
	}
	try {
		const config = JSON.parse(readFileSync(configPath, 'utf8')) as {
			webserver_port?: string | number;
		};
		return Number(config.webserver_port) || DEFAULT_WEBSERVER_PORT;
	} catch {
		return DEFAULT_WEBSERVER_PORT;
	}
}

const webserver_port = getWebserverPort();

export default {
	'^/(app|api|assets|files|private)': {
		target: `http://127.0.0.1:${webserver_port}`,
		ws: true,
		router: function (req: { headers?: { host?: string } }) {
			const site_name = req.headers?.host?.split(':')[0];
			return `http://${site_name ?? 'localhost'}:${webserver_port}`;
		}
	}
};
