/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './allocatr/templates/*.html',
    './allocatr/templates/**/*.html',
    './allocatr/templates/**/**/*.html',
    './allocatr/templates/**/**/**/*.html',
    './allocatr/static/js/project.js',
  ],
  theme: {
    extend: {
      colors: {
        "accent": "#1c64f2",
        "accentLight": "#3f83f8",
        "accentLightest": "#76a9fa",
        "accentDark": "#1a56db",
        "accentDarkest": "#1e429f",
      },
      screens: {
        'xs': '475px',
        '3xl': '1600px',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require("daisyui"),
  ],
}
