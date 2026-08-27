export {};

declare global {
	interface Window {
		frappe?: {
			csrf_token?: string;
		};
	}
}
