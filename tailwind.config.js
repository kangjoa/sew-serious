const colors = require('tailwindcss/colors');

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './sewing_app/templates/**/*.html',
    './static/**/*.js',
    './static/**/*.css',
  ],
  theme: {
    screens: {
      sm: '480px',
      md: '768px',
      lg: '976px',
      xl: '1440px',
    },
    colors: {
      charcoal: '#1e293b',
      blue: '#A0E8E5',
      'dark-blue': '#0369a1',
      purple: '#C9A0FF',
      'dark-purple': '#7851A9',
      pink: {
        50: '#fdf2f8',
        100: '#fce7f3',
        600: '#FFD3E0',
      },
      orange: {
        50: '#fff8f1',
        100: '#feecdf',
        200: '#fcd9bd',
        600: '#FFB97D',
      },
      green: '#A6FFCB',
      yellow: '#FFFACD',
      'gray-dark': '#6B6E70',
      gray: '#BDC0C2',
      'gray-light': '#EDEDED',
      white: colors.white,
    },
    fontFamily: {
      sans: ['Graphik', 'sans-serif'],
      serif: ['Merriweather', 'serif'],
    },
    extend: {
      fontFamily: { display: 'Cambria, ui-serif' },
      spacing: {
        128: '32rem',
        144: '36rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
    },
  },
  plugins: [require('@tailwindcss/forms')],
};
