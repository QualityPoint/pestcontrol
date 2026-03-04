import './index.css';
import { createApp, reactive } from 'vue';
import App from './App.vue';

import router from './router';
import { FrappeUI, frappeRequest, setConfig } from 'frappe-ui';
import call from './controllers/call';
import socket from './controllers/socket';
import Auth from './controllers/auth';

const app = createApp(App);
const auth = reactive(new Auth());

// Configure frappe-ui to use frappeRequest for all resources
setConfig('resourceFetcher', frappeRequest);

// Plugins
// Disable frappe-ui's built-in socket (it hardcodes port 9000).
// We provide our own $socket below, which connects via window.location.origin
// so the Vite proxy can forward it to the correct socketio_port (9006).
app.use(FrappeUI, { socketio: false });
app.use(router);

// Global Properties,
// components can inject this
app.provide('$auth', auth);
app.provide('$call', call);
app.provide('$socket', socket);


// Configure route gaurds
router.beforeEach(async (to, from, next) => {
	if (to.matched.some((record) => !record.meta.isLoginPage)) {
		// this route requires auth, check if logged in
		// if not, redirect to login page.
		if (!auth.isLoggedIn) {
			next({ name: 'Login', query: { route: to.path } });
		} else {
			next();
		}
	} else {
		if (auth.isLoggedIn) {
			next({ name: 'Home' });
		} else {
			next();
		}
	}
});

app.mount("#app");
