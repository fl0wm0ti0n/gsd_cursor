# Sprint S0001

## Goal

Deliver a working vertical slice: filtered item list with detail panel, powered by a shared-schema REST API. Users can filter items by status/category/date, view details in a slide-over panel, and create/update items — all validated end-to-end with shared Zod schemas.

## Scope

- **US-0002** — Filter Bar with Instant Results
- **US-0003** — Slide-Over Detail Panel
- **US-0004** — Empty-State & Filter Awareness

## User Stories → Task Mapping

| Story   | Tasks                          |
|---------|--------------------------------|
| US-0002 | T-015, T-016, T-017, T-018, T-019 |
| US-0003 | T-010, T-016, T-020           |
| US-0004 | T-021                          |
| Infra   | T-001, T-002, T-003, T-007, T-008, T-022 |

## Build Order (dependency chain)

```
T-001 Scaffold workspace
  └─ T-002 Shared Zod schemas + types
      ├─ T-003 tsconfig path aliases
      ├─ T-004 Backend validation middleware
      └─ T-005 Frontend form validation setup
          │
  T-007 Express server + health check ─┐
  T-008 Drizzle schema + SQLite setup ──┤
  T-014 Error envelope ────────────────┘
          │
  T-009 GET /items (filtered + paginated)
  T-010 GET /items/:id
  T-011 POST /items
  T-012 PATCH /items/:id
  T-013 DELETE /items/:id (soft)
          │
  T-015 React + Vite + Tailwind shell ─┐
  T-022 Vite dev proxy ────────────────┘
          │
  T-016 Typed API client + TanStack Query hooks
  T-006 Response validation on API client
          │
  T-017 FilterBar component
  T-018 useFilters hook (URL sync)
  T-019 ItemList component
  T-020 DetailPanel component
  T-021 EmptyState component
```

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Shared schema drift if `/shared` is not built first | Medium | High | npm workspaces build order: shared → backend → frontend |
| CORS misconfiguration between SPA and API | Medium | Low | Vite proxy for dev; explicit CORS middleware for prod |
| SQLite → PostgreSQL dialect differences | Low | Medium | Drizzle ORM abstracts dialect; test against both in CI |
| Filter query params exceed URL length | Low | Low | Start with 4 dimensions; add POST filter fallback if needed |

## Definition of Done

- All 22 tasks complete and checked off in `tasks.md`
- Shared schemas consumed by both frontend and backend without duplication
- API returns structured error envelope for validation failures
- Filter bar updates list instantly; active filters reflected in URL
- Detail panel opens/closes with keyboard navigation (arrows, Escape)
- Empty state renders with "Reset filters" action when no results match
