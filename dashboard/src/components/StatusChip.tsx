import { Chip } from '@mui/material';

const STATUS_COLOR: Record<string, 'success' | 'error' | 'warning' | 'default'> = {
	Paid: 'success',
	Completed: 'success',
	Closed: 'success',
	Draft: 'default',
	'To Bill': 'warning',
	'To Deliver and Bill': 'warning',
	Overdue: 'error',
	Cancelled: 'error',
	Unpaid: 'warning'
};

export default function StatusChip({ status }: { status?: string }) {
	if (!status) return null;
	const color = STATUS_COLOR[status] ?? 'default';
	return <Chip label={status} color={color} size="small" />;
}
