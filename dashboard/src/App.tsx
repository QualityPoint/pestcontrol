import { useMemo, useState } from 'react';
import {
	ThemeProvider,
	CssBaseline,
	Box,
	AppBar,
	Toolbar,
	Typography,
	Drawer,
	List,
	ListItemButton,
	ListItemIcon,
	ListItemText,
	IconButton,
	Avatar,
	Tooltip,
	useMediaQuery
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import HomeIcon from '@mui/icons-material/Home';
import DashboardIcon from '@mui/icons-material/SpaceDashboard';
import ReceiptLongIcon from '@mui/icons-material/ReceiptLong';
import RequestQuoteIcon from '@mui/icons-material/RequestQuote';
import DescriptionIcon from '@mui/icons-material/Description';
import PersonIcon from '@mui/icons-material/Person';
import { createDashboardTheme } from './theme';
import { getInitials } from './utils/initials';
import Overview from './pages/Overview';
import PortalDocumentList from './components/PortalDocumentList';
import DocumentDetail from './pages/DocumentDetail';
import AccountPage from './pages/AccountPage';
import type { PortalListRow } from './api/portal';

export type PageType = 'overview' | 'list' | 'detail' | 'account';

const DRAWER_WIDTH = 260;

const NAV_ITEMS = [
	{ href: '/portal', label: 'Overview', icon: <DashboardIcon /> },
	{ href: '/orders', label: 'Orders', icon: <ReceiptLongIcon /> },
	{ href: '/quotations', label: 'Quotations', icon: <RequestQuoteIcon /> },
	{ href: '/invoices', label: 'Invoices', icon: <DescriptionIcon /> },
	{ href: '/me', label: 'My Account', icon: <PersonIcon /> }
];

interface AppProps {
	direction: 'ltr' | 'rtl';
	pageType: PageType;
	doctype?: string;
	docName?: string;
	listRows: PortalListRow[];
	detailDoc?: Record<string, unknown>;
	account: {
		fullName?: string;
		email?: string;
		avatarUrl?: string;
	};
}

const LIST_TITLES: Record<string, { title: string; basePath: string }> = {
	'Sales Order': { title: 'Orders', basePath: '/orders' },
	Quotation: { title: 'Quotations', basePath: '/quotations' },
	'Sales Invoice': { title: 'Invoices', basePath: '/invoices' }
};

function currentPath() {
	return window.location.pathname.replace(/\/+$/, '') || '/';
}

function DashboardShell(props: AppProps) {
	const isDesktop = useMediaQuery('(min-width:900px)');
	const [mobileOpen, setMobileOpen] = useState(false);
	const path = currentPath();

	const nav = (
		<List sx={{ pt: 2 }}>
			{NAV_ITEMS.map((item) => {
				const active = item.href === '/portal' ? path === '/portal' : path.startsWith(item.href);
				return (
					<ListItemButton
						key={item.href}
						component="a"
						href={item.href}
						sx={{
							mx: 1,
							borderRadius: 3,
							...(active && {
								backgroundColor: 'secondary.main',
								color: 'secondary.contrastText',
								'& .MuiListItemIcon-root': { color: 'secondary.contrastText' }
							})
						}}
					>
						<ListItemIcon>{item.icon}</ListItemIcon>
						<ListItemText primary={item.label} />
					</ListItemButton>
				);
			})}
		</List>
	);

	const listMeta = props.doctype ? LIST_TITLES[props.doctype] : undefined;

	return (
		<Box sx={{ display: 'flex', minHeight: '100vh' }}>
			<AppBar position="fixed" sx={{ zIndex: (t) => t.zIndex.drawer + 1 }} elevation={0}>
				<Toolbar>
					{!isDesktop && (
						<IconButton edge="start" onClick={() => setMobileOpen(true)} sx={{ mr: 2 }}>
							<MenuIcon />
						</IconButton>
					)}
					<Typography variant="h6" component="div" sx={{ fontWeight: 700, flexGrow: 1 }}>
						My Dashboard
					</Typography>

					<Tooltip title="Back to site">
						<IconButton component="a" href="/" sx={{ color: 'inherit' }}>
							<HomeIcon />
						</IconButton>
					</Tooltip>
					<Tooltip title="My Account">
						<IconButton component="a" href="/me" sx={{ ml: 1 }}>
							<Avatar
								src={props.account.avatarUrl}
								sx={{ width: 32, height: 32, bgcolor: 'secondary.main', fontSize: 14 }}
							>
								{getInitials(props.account.fullName, props.account.email)}
							</Avatar>
						</IconButton>
					</Tooltip>
				</Toolbar>
			</AppBar>

			<Drawer
				variant={isDesktop ? 'permanent' : 'temporary'}
				open={isDesktop ? true : mobileOpen}
				onClose={() => setMobileOpen(false)}
				sx={{
					width: DRAWER_WIDTH,
					flexShrink: 0,
					'& .MuiDrawer-paper': { width: DRAWER_WIDTH, boxSizing: 'border-box' }
				}}
			>
				<Toolbar />
				{nav}
			</Drawer>

			<Box
				component="main"
				sx={{ flexGrow: 1, p: { xs: 2, md: 4 }, width: { md: `calc(100% - ${DRAWER_WIDTH}px)` } }}
			>
				<Toolbar />
				{props.pageType === 'overview' && <Overview />}
				{props.pageType === 'list' && listMeta && (
					<PortalDocumentList rows={props.listRows} title={listMeta.title} basePath={listMeta.basePath} />
				)}
				{props.pageType === 'detail' && props.detailDoc && (
					<DocumentDetail doc={props.detailDoc} backHref={props.doctype ? LIST_TITLES[props.doctype]?.basePath : undefined} />
				)}
				{props.pageType === 'account' && <AccountPage {...props.account} />}
			</Box>
		</Box>
	);
}

export default function App(props: AppProps) {
	const theme = useMemo(() => createDashboardTheme(props.direction), [props.direction]);

	return (
		<ThemeProvider theme={theme}>
			<CssBaseline />
			<DashboardShell {...props} />
		</ThemeProvider>
	);
}
