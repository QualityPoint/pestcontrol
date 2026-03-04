import call from './call';

export default class Auth {
    isLoggedIn: boolean;
    user: string | null;
    user_image: string | null;

    constructor() {
        this.isLoggedIn = false;
        this.user = null;
        this.user_image = null;

        const cookie = Object.fromEntries(
            document.cookie
                .split('; ')
                .filter(Boolean)
                .map((part) => part.split('='))
                .map((d) => [d[0], decodeURIComponent(d[1])])
        );

        this.isLoggedIn = !!(cookie.user_id && cookie.user_id !== 'Guest');
    }

    async login(email: string, password: string) {
        const res = await call('login', { usr: email, pwd: password });
        if (res) {
            this.isLoggedIn = true;
            return res;
        }
        return false;
    }

    async logout() {
        await call('logout');
        this.isLoggedIn = false;
        window.location.reload();
    }
}
