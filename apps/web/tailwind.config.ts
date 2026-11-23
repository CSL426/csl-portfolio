import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{vue,ts,tsx}'],
  theme: {
    extend: {
      screens: {
        // Small-phone steps for the nav pill. Raw queries: Tailwind 3 rejects arbitrary
        // max-[…rem] variants because the default screens are in px.
        narrow: { raw: '(max-width: 22.5rem)' },
        tiny: { raw: '(max-width: 21rem)' },
      },
      fontFamily: {
        display: ['var(--font-display)'],
        mono: ['var(--font-mono)'],
        sans: [
          'Noto Sans TC',
          'Microsoft JhengHei',
          'PingFang TC',
          'Segoe UI',
          'system-ui',
          'sans-serif',
        ],
      },
      colors: {
        // Semantic tokens from src/styles/tokens.css. `brand` below stays as-is:
        // the A4 resume components are matched to the PDF and must not shift.
        paper: 'var(--color-paper)',
        'paper-2': 'var(--color-paper-2)',
        'surface-subtle': 'var(--color-surface-subtle)',
        ink: 'var(--color-ink)',
        'ink-hover': 'var(--color-ink-hover)',
        'ink-2': 'var(--color-ink-2)',
        'on-ink': 'var(--color-on-ink)',
        rule: 'var(--color-rule)',
        'rule-strong': 'var(--color-rule-strong)',
        accent: 'var(--color-accent)',
        'accent-soft': 'var(--color-accent-soft)',
        focus: 'var(--color-focus)',
        danger: 'var(--color-danger)',
        'status-live-bg': 'var(--color-status-live-bg)',
        'status-live-fg': 'var(--color-status-live-fg)',
        'status-soon-bg': 'var(--color-status-soon-bg)',
        'status-soon-fg': 'var(--color-status-soon-fg)',
        'status-muted-bg': 'var(--color-status-muted-bg)',
        'status-muted-fg': 'var(--color-status-muted-fg)',
        brand: {
          start: '#76abd6',
          end: '#8ebfe5',
          sidebar: '#e8edf3',
          page: '#edf1f5',
          ink: '#1f2633',
          muted: '#4a5568',
        },
      },
      boxShadow: {
        card: '0 8px 18px rgba(0, 0, 0, 0.08)',
        page: '0 20px 45px rgba(0, 0, 0, 0.18)',
        profile: '0 16px 30px rgba(111, 150, 196, 0.22)',
      },
    },
  },
  plugins: [],
} satisfies Config
