# Lente

Static teaching website for the Lente project, combining curated learning paths, editorial pages, and classroom projection flow.

## Project structure

- `index.html` — site landing page
- `apresentar/`, `biblioteca/`, `caderno/`, `projetos/`, etc. — themed sections and learning paths
- `assets/` — shared JavaScript and CSS used by the site
- `img/` — images and media assets
- `docs/` — notes and QA materials

## Local preview

This is a static site, so it can be served with any simple web server:

```bash
python -m http.server 8000
```

Then open:

- http://localhost:8000/

## Important behavior

- Site state is stored in the browser via `localStorage`.
- Projection actions are handled by `assets/projection-launcher.js` and `assets/projection.js`.
- Pages rely on client-side scripts for navigation, progress tracking, and classroom projection support.

## Improvement focus

- Keep section metadata and page titles consistent as the site grows.
- Review accessibility labels, keyboard flow, and focus states across the lesson pages.
- Centralize repeated CSS/JS patterns if the site is expanded with more sections.
- Keep projection and local-storage logic resilient to DOM changes and missing elements.
