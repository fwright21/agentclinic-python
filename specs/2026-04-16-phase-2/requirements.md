# Phase 2 — Requirements

## Goal
Shared base layout rendered via Jinja2. All routes render inside it. Plain CSS only — no JS build step, no frameworks.

## Requirements

1. Jinja2 templating configured in FastAPI
2. Shared layout: `base.html` with header, nav, main content block, footer
3. Nav placeholder links: Agents, Ailments, Appointments, Dashboard (no routes yet — `href="#"`)
4. Plain CSS in `static/css/style.css` — reset + custom properties + typography
5. Static file serving configured in FastAPI
6. `/` route renders inside the shared layout

## Out of scope
- Real nav routes (placeholders only)
- JavaScript
- Dark mode
- Responsive/mobile (later phase)

---

## Design System

### Colours — base palette
| Token | Use | Hex |
|---|---|---|
| `--color-bg` | Page background | `#F8FAFC` |
| `--color-surface` | Cards, panels | `#FFFFFF` |
| `--color-border` | Borders, dividers | `#E2E8F0` |
| `--color-primary` | Actions, links, active nav | `#2563EB` |
| `--color-text` | Primary text | `#0F172A` |
| `--color-text-muted` | Secondary text | `#64748B` |

### Colours — status
| Token | Use | Hex |
|---|---|---|
| `--status-resolved` | Resolved | `#10B981` |
| `--status-active` | Pending / Active | `#3B82F6` |
| `--status-recurring` | Recurring | `#F59E0B` |
| `--status-chronic` | Chronic | `#EF4444` |
| `--status-unknown` | No data | `#94A3B8` |

### Colours — severity
| Token | Use | Hex |
|---|---|---|
| `--severity-low` | Low | `#22C55E` |
| `--severity-medium` | Medium | `#F59E0B` |
| `--severity-high` | High | `#F97316` |
| `--severity-critical` | Critical | `#DC2626` |

### Typography
| Role | Font | Weight |
|---|---|---|
| Headings | Inter or DM Sans | 600–700 |
| Body / UI | Inter | 400 |
| Mono (IDs, token counts, visit numbers) | JetBrains Mono or Fira Code | 400 |

### Layout
- Max content width: `1200px`, centred
- Spacing base: `8px` grid
- Style: flat / minimal, subtle borders, no shadows

### Header
- Logo / app name left: **AgentClinic**
- Nav links right: Agents · Ailments · Appointments · Dashboard

### Footer
- Minimal: app name + version
