import { io } from 'socket.io-client';

// Connects via the same origin so the Vite /socket.io proxy
// forwards to the real Frappe socketio port (see proxyOptions.ts).
const socket = io(window.location.origin, {
    withCredentials: true,
    reconnectionAttempts: 5,
});

export default socket;
