// frontend/tailwind.config.js

module.exports = {
  darkMode: 'media', // Enable dark mode support based on user's OS setting
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
};