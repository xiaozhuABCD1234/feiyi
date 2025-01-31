/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 古风配色
        gufeng_1: '#f2e7e5',
        gufeng_2: '#1D4C50',
        gufeng_3: '#D3A488',
        gufeng_4: '#BDAEBD',
      }
    },
  },
  plugins: [],
}

