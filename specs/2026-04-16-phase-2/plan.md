# Phase 2 — Plan

## File structure
```
agentclinic-python/
  src/
    main.py          (update — mount static, configure Jinja2, update GET /)
    templates/
      base.html      (create)
      index.html     (create)
  static/
    css/
      style.css      (create)
```

## Steps

1. Install Jinja2 (already in requirements.txt — confirm)

2. Update `src/main.py`:
   - Mount `StaticFiles` at `/static`
   - Configure `Jinja2Templates` pointing to `src/templates`
   - Update `GET /` to render `index.html` via `TemplateResponse`

3. Create `src/templates/base.html`:
   - `<head>`: link to `/static/css/style.css`, Inter font via Google Fonts
   - `<header>`: app name left, nav links right (href="#")
   - `<main>`: Jinja2 `{% block content %}{% endblock %}`
   - `<footer>`: "AgentClinic v0.1"

4. Create `src/templates/index.html`:
   - Extends `base.html`
   - Content block: `<h1>AgentClinic is open for business</h1>`

5. Create `static/css/style.css`:
   - CSS reset (box-sizing, margin, padding)
   - Custom properties for all colour tokens and typography
   - Base typography: Inter 16px, line-height 1.5, slate-900
   - Layout: max-width 1200px, centred, 8px spacing grid
   - Header: flex, space-between, border-bottom
   - Nav: flex gap, links styled with primary colour on hover/active
   - Main: padding top/bottom
   - Footer: minimal, muted text, border-top
