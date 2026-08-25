import { Box, Card, CardContent, Typography, Avatar, List, ListItemButton, ListItemIcon, ListItemText, Divider } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import LockIcon from '@mui/icons-material/Lock';
import LogoutIcon from '@mui/icons-material/Logout';
import { getInitials } from '../utils/initials';

interface AccountPageProps {
	fullName?: string;
	email?: string;
	avatarUrl?: string;
}

export default function AccountPage({ fullName, email, avatarUrl }: AccountPageProps) {
	const initials = getInitials(fullName, email);
	return (
		<Box sx={{ maxWidth: 480 }}>
			<Typography variant="h4" sx={{ mb: 3 }}>
				My Account
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
							<ListItemText primary="Edit Profile" />
						</ListItemButton>
						<ListItemButton component="a" href="/update-password">
							<ListItemIcon>
								<LockIcon />
							</ListItemIcon>
							<ListItemText primary="Reset Password" />
						</ListItemButton>
						<ListItemButton component="a" href="/api/method/logout">
							<ListItemIcon>
								<LogoutIcon />
							</ListItemIcon>
							<ListItemText primary="Logout" />
						</ListItemButton>
					</List>
				</CardContent>
			</Card>
		</Box>
	);
}
