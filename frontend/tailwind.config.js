export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        primary: { 50: '#eff6ff', 500: '#2563eb', 600: '#1d4ed8', 700: '#1e40af' },
        success: { 50: '#f0fdf4', 600: '#16a34a' },
        warning: { 50: '#fffbeb', 600: '#d97706' },
        danger: { 500: '#ef4444', 600: '#dc2626' },
      },
    },
  },
  plugins: [],
};