import { frappeRequest } from 'frappe-ui';

/**
 * Thin wrapper matching doppio's call(method, args) API,
 * backed by frappe-ui's frappeRequest.
 */
export default function call(
    method: string,
    args?: Record<string, any>
): Promise<any> {
    return frappeRequest({
        url: `/api/method/${method}`,
        type: 'POST',
        params: args || {},
    });
}
