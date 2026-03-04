const common_site_config = require('../../../sites/common_site_config.json');
const { webserver_port, socketio_port } = common_site_config;

// The actual Frappe site name — must match a directory under sites/
const FRAPPE_SITE_NAME = process.env.VITE_SITE_NAME || 'site.local';

export default {
	'^/(app|api|assets|files|private)': {
		target: `http://127.0.0.1:${webserver_port}`,
		ws: true,
		router: function (req: { headers: { host: string } }) {
			return `http://${FRAPPE_SITE_NAME}:${webserver_port}`;
		},
		configure: (proxy: any) => {
			proxy.on('proxyReq', (proxyReq: any) => {
				// Override whatever hostname the browser sent; Frappe needs the real site name
				proxyReq.setHeader('X-Frappe-Site-Name', FRAPPE_SITE_NAME);
			});
		}
	},
	'/socket.io': {
		target: `http://127.0.0.1:${socketio_port || 9006}`,
		ws: true,
		changeOrigin: true
	}
};
