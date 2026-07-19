import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{vue,ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
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
