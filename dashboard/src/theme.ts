import { createTheme } from '@mui/material/styles';

// Brand tokens, kept identical to pestcontrol/public/website/css/custom.css's
// :root block and the portal.css reskin — this SPA is its own document and
// doesn't inherit either stylesheet, so the values are repeated here.
const brand = {
	primary: '#002F47',
	secondary: '#F5F7F2',
	text: '#3D5A6A',
	accent: '#217D39',
	white: '#FFFFFF',
	divider: '#002F471A',
	error: 'rgb(230, 87, 87)',
	warning: '#B8860B'
};

export function createDashboardTheme(direction: 'ltr' | 'rtl') {
	return createTheme({
		direction,
		palette: {
			mode: 'light',
			primary: { main: brand.primary, contrastText: brand.white },
			secondary: { main: brand.accent, contrastText: brand.white },
			error: { main: brand.error },
			warning: { main: brand.warning },
			background: { default: brand.secondary, paper: brand.white },
			text: { primary: brand.text, secondary: brand.primary },
			divider: brand.divider
		},
		typography: {
			fontFamily: '"IBM Plex Sans Arabic", sans-serif',
			h1: { fontWeight: 700, color: brand.primary },
			h2: { fontWeight: 700, color: brand.primary },
			h3: { fontWeight: 700, color: brand.primary },
			h4: { fontWeight: 700, color: brand.primary },
			h5: { fontWeight: 700, color: brand.primary },
			h6: { fontWeight: 700, color: brand.primary }
		},
		shape: {
			borderRadius: 16
		},
		components: {
			MuiCard: {
				styleOverrides: {
					root: {
						borderRadius: 24,
						border: `1px solid ${brand.divider}`,
						boxShadow: '0px 0px 30px 0px #002F471A'
					}
				}
			},
			MuiButton: {
				styleOverrides: {
					root: {
						borderRadius: 100,
						textTransform: 'none',
						fontWeight: 700,
						paddingInline: 24
					}
				}
			},
			MuiChip: {
				styleOverrides: {
					root: {
						borderRadius: 100,
						fontWeight: 600
					}
				}
			},
			MuiAppBar: {
				styleOverrides: {
					root: {
						backgroundColor: brand.white,
						color: brand.primary,
						boxShadow: '0px 0px 11.8px 0px #0000000F'
					}
				}
			},
			MuiDrawer: {
				styleOverrides: {
					paper: {
						backgroundColor: brand.white,
						borderInlineEnd: `1px solid ${brand.divider}`
					}
				}
			}
		}
	});
}

export default brand;
