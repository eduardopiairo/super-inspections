import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";

const root = fileURLToPath(new URL(".", import.meta.url));

export default defineConfig({
  build: {
    outDir: "../backend/static",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: `${root}index.html`,
        templates: `${root}templates.html`,
        inspections: `${root}inspections.html`,
        schedules: `${root}schedules.html`,
        actions: `${root}actions.html`,
        settings: `${root}settings.html`,
        "settings-users": `${root}settings/users.html`,
        "settings-sites": `${root}settings/sites.html`,
      },
    },
  },
  server: {
    proxy: {
      "/health": "http://localhost:8000",
      "/inspections/": "http://localhost:8000",
      "/templates/": "http://localhost:8000",
      "/schedules/": "http://localhost:8000",
      "/actions/": "http://localhost:8000",
      "/users/": "http://localhost:8000",
      "/sites/": "http://localhost:8000",
    },
  },
});
