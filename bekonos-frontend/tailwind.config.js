export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#20467A",
        accent: "#5376A6",
        yellow: "#FFD94A",
        aqua: "#60C6C9",
        background: "#F6F8FA",
        dark: "#2D3137",
      },
      fontFamily: {
        headline: ["Montserrat", "Inter", "sans-serif"],
        body: ["Inter", "Nunito", "Open Sans", "sans-serif"],
      },
    },
  },
  plugins: [],
};
