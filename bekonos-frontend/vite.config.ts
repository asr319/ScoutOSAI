import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

// https://vite.dev/config/
export default defineConfig({
  // When deploying to GitHub Pages the site is served from `/bekonOS`.
  // Setting the base path ensures asset URLs resolve correctly.
  base: "/bekonOS/",
  plugins: [
    react(),
    VitePWA({
      filename: "sw.ts",
      manifestFilename: "manifest.json",
      registerType: "autoUpdate",
    }),
  ],
  test: {
    environment: "jsdom",
  },
});
