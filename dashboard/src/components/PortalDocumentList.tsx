import { Card, CardContent, Typography, List, ListItemButton, ListItemText, Box, Stack } from '@mui/material';
import dayjs from 'dayjs';
import type { PortalListRow } from '../api/portal';
import StatusChip from './StatusChip';

interface PortalDocumentListProps {
	rows: PortalListRow[];
	title: string;
	basePath: string;
}

export default function PortalDocumentList({ rows, title, basePath }: PortalDocumentListProps) {
	return (
		<Box>
			<Typography variant="h4" sx={{ mb: 3 }}>
				{title}
			</Typography>

			<Card>
				<CardContent sx={{ p: 0, '&:last-child': { pb: 0 } }}>
					{rows.length === 0 && (
						<Box sx={{ p: 4, textAlign: 'center' }}>
							<Typography color="text.secondary">No {title.toLowerCase()} yet.</Typography>
						</Box>
					)}

					<List disablePadding>
						{rows.map((row) => (
							<ListItemButton
								key={row.name}
								component="a"
								href={`${basePath}/${encodeURIComponent(row.name)}`}
								divider
							>
								<ListItemText
									primary={row.name}
									secondary={
										row.transaction_date || row.posting_date
											? dayjs((row.transaction_date ?? row.posting_date) as string).format('DD MMM YYYY')
											: undefined
									}
								/>
								<Stack direction="row" spacing={2} alignItems="center">
									{typeof row.grand_total === 'number' && (
										<Typography sx={{ fontWeight: 600 }}>
											{row.currency ?? ''} {row.grand_total.toLocaleString()}
										</Typography>
									)}
									<StatusChip status={row.status} />
								</Stack>
							</ListItemButton>
						))}
					</List>
				</CardContent>
			</Card>
		</Box>
	);
}
