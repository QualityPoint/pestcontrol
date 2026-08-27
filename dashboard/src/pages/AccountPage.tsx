import { Box, Card, CardContent, Typography, Avatar, List, ListItemButton, ListItemIcon, ListItemText, Divider } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import LockIcon from '@mui/icons-material/Lock';
import LogoutIcon from '@mui/icons-material/Logout';
import { getInitials } from '../utils/initials';
import { t, type Lang } from '../i18n';

interface AccountPageProps {
	fullName?: string;
	email?: string;
	avatarUrl?: string;
	lang: Lang;
}

async function handleLogout(e: React.MouseEvent) {
	e.preventDefault();
	// /api/method/logout is a whitelisted RPC method (POST-only) — a plain
	// <a href> GET navigation gets rejected with a 403 "Not Permitted"
	// (frappe.throw_permission_error via is_valid_http_method), and since
	// the request never runs, the session is never actually cleared.
	await fetch('/api/method/logout', {
		method: 'POST',
		credentials: 'include',
		headers: { 'X-Frappe-CSRF-Token': window.frappe?.csrf_token ?? '' }
	});
	window.location.href = '/';
}

export default function AccountPage({ fullName, email, avatarUrl, lang }: AccountPageProps) {
	const s = t(lang);
	const initials = getInitials(fullName, email);
	return (
		<Box sx={{ maxWidth: 480 }}>
			<Typography variant="h4" sx={{ mb: 3 }}>
				{s.myAccountTitle}
			</Typography>

			<Card>
				<CardContent sx={{ p: 0 }}>
					<Box sx={{ p: 4, textAlign: 'center', backgroundColor: 'background.default' }}>
						<Avatar src={avatarUrl} sx={{ width: 72, height: 72, mx: 'auto', mb: 2, bgcolor: 'secondary.main' }}>
							{initials}
						</Avatar>
						<Typography variant="h6">{fullName}</Typography>
						<Typography color="text.secondary">{email}</Typography>
					</Box>

					<Divider />

					<List disablePadding>
						<ListItemButton component="a" href="/update-profile">
							<ListItemIcon>
								<EditIcon />
							</ListItemIcon>
							<ListItemText primary={s.editProfile} />
						</ListItemButton>
						<ListItemButton component="a" href="/update-password">
							<ListItemIcon>
								<LockIcon />
							</ListItemIcon>
							<ListItemText primary={s.resetPassword} />
						</ListItemButton>
						<ListItemButton component="a" href="/api/method/logout" onClick={handleLogout}>
							<ListItemIcon>
								<LogoutIcon />
							</ListItemIcon>
							<ListItemText primary={s.logout} />
						</ListItemButton>
					</List>
				</CardContent>
			</Card>
		</Box>
	);
}
