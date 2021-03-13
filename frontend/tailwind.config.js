const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
  purge: ['../**/*.html', '../**/*.js'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter var', ...defaultTheme.fontFamily.sans],
      },
    },
  },
  plugins: [require('@tailwindcss/forms'), require('@tailwindcss/typography')],
};
