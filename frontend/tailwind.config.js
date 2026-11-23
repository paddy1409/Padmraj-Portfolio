module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  theme: {
    extend: {
      fontFamily: {
        display: ["Syne", "sans-serif"],
        sans: ['"Plus Jakarta Sans"', "sans-serif"],
        mono: ['"JetBrains Mono"', "monospace"],
      },
      colors: {
        paper: "#FBFBF9",
        paperalt: "#F3F3EF",
        ink: "#0F1216",
        ink2: "#525866",
        ink3: "#8A919E",
        line: "#E5E5DF",
        accent: "#0055FF",
        accentdark: "#0043CC",
        accsoft: "#EEF4FF",
        term: "#0B0E14",
      },
      animation: {
        marquee: "marquee 38s linear infinite",
      },
      keyframes: {
        marquee: {
          "0%": { transform: "translateX(0)" },
          "100%": { transform: "translateX(-50%)" },
        },
      },
    },
  },
  plugins: [],
};
