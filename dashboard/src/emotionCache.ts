import createCache from '@emotion/cache';
import rtlPlugin from 'stylis-plugin-rtl';
import { prefixer } from 'stylis';

// MUI's `theme.direction: 'rtl'` alone only changes a handful of components'
// internal logic (Popper placement, Select icon side) — it does not flip
// the CSS properties (`margin-left`/`padding-inline-start`/text-align/etc.)
// that `sx` props actually emit. That requires routing Emotion's output
// through stylis-plugin-rtl, per MUI's own RTL guide.
export function createEmotionCache(direction: 'ltr' | 'rtl') {
	if (direction === 'rtl') {
		return createCache({ key: 'muirtl', stylisPlugins: [prefixer, rtlPlugin] });
	}
	return createCache({ key: 'mui' });
}
