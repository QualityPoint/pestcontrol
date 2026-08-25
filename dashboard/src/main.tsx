import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App, { type PageType } from './App';
import type { PortalListRow } from './api/portal';

const rootEl = document.getElementById('root');

if (rootEl) {
	const pageType = (rootEl.dataset.pageType as PageType | undefined) ?? 'overview';
	const doctype = rootEl.dataset.doctype;
	const docName = rootEl.dataset.name;
	const direction = (document.documentElement.getAttribute('dir') as 'ltr' | 'rtl') || 'ltr';

	const dataEl = document.getElementById('portal-data');
	const embedded = dataEl?.textContent ? JSON.parse(dataEl.textContent) : undefined;

	const listRows: PortalListRow[] = pageType === 'list' && Array.isArray(embedded) ? embedded : [];
	const detailDoc: Record<string, unknown> | undefined =
		pageType === 'detail' && embedded && !Array.isArray(embedded) ? embedded : undefined;

	createRoot(rootEl).render(
		<StrictMode>
			<App
				direction={direction}
				pageType={pageType}
				doctype={doctype}
				docName={docName}
				listRows={listRows}
				detailDoc={detailDoc}
				account={{
					fullName: rootEl.dataset.fullName,
					email: rootEl.dataset.email,
					avatarUrl: rootEl.dataset.avatarUrl
				}}
			/>
		</StrictMode>
	);
}
