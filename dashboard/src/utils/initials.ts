export function getInitials(fullName?: string, email?: string): string {
	const source = fullName || email || '';
	return source
		.split(/\s+/)
		.filter(Boolean)
		.slice(0, 2)
		.map((part) => part[0]?.toUpperCase())
		.join('');
}
