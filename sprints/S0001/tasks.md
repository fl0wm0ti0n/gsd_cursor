# Tasks — Sprint S0001

## Shared Schema

- [ ] **T-001** Scaffold npm workspace with `frontend/`, `backend/`, `shared/` packages and root `package.json` with workspaces config
- [ ] **T-002** Create shared Zod schemas: `shared/schemas/item.schema.ts` (CreateItemSchema, UpdateItemSchema, ItemStatus enum) and `shared/schemas/filter.schema.ts` (ItemFilterSchema with pagination, sort, date range); export inferred TypeScript types from `shared/types/`
- [ ] **T-003** Configure `tsconfig.base.json` with path aliases (`@shared/*`) and per-package tsconfig files extending it

## Validation

- [ ] **T-004** Implement backend validation middleware (`backend/src/middleware/validate.ts`) — generic Zod safeParse for body, query, and params; returns 400 with structured error details on failure
- [ ] **T-005** Configure frontend form validation with `@hookform/resolvers/zod` using shared CreateItemSchema and UpdateItemSchema
- [ ] **T-006** Add response validation on frontend API client — parse API responses through shared Zod schemas to catch contract drift at runtime

## API

- [ ] **T-007** Stand up Express 5 server (`backend/src/server.ts`) with health check endpoint (`GET /api/v1/health`), CORS middleware, JSON body parser, and global error handler
- [ ] **T-008** Create Drizzle ORM schema (`backend/src/db/schema.ts`) with items table (id, title, status, category, description, metadata, createdAt, updatedAt, deletedAt) and SQLite connection for dev
- [ ] **T-009** Implement `GET /api/v1/items` — filtered list with status, category, dateFrom/dateTo, search, pagination (page/pageSize), sort, and order; uses validate middleware with ItemFilterSchema; returns data array + meta object
- [ ] **T-010** Implement `GET /api/v1/items/:id` — single item with full details; returns 404 with error envelope if not found
- [ ] **T-011** Implement `POST /api/v1/items` — create item; validates body with CreateItemSchema; returns 201 with created item
- [ ] **T-012** Implement `PATCH /api/v1/items/:id` — partial update; validates body with UpdateItemSchema; returns updated item or 404
- [ ] **T-013** Implement `DELETE /api/v1/items/:id` — soft delete (set deletedAt); returns 204 No Content or 404
- [ ] **T-014** Implement structured error envelope middleware — consistent `{ error: { code, message, details } }` shape for VALIDATION_ERROR, NOT_FOUND, and INTERNAL_ERROR

## UI

- [ ] **T-015** Scaffold React 18 + Vite + TypeScript app in `frontend/`; install and configure Tailwind CSS, React Router v6 with a root layout route
- [ ] **T-016** Create typed API client (`frontend/src/api/client.ts`) and TanStack Query hooks (`useItems`, `useItem`, `useCreateItem`, `useUpdateItem`, `useDeleteItem`) wrapping all endpoints
- [ ] **T-017** Build `FilterBar` component — horizontal chip-based multi-select for status, category, and date range (US-0002); active filters shown as filled chips with "x" dismiss; "Clear all" link when 2+ filters active
- [ ] **T-018** Build `useFilters` hook — reads/writes filter state to URL search params via React Router `useSearchParams`; provides `setFilter`, `removeFilter`, `clearAll`, and `activeFilterCount`
- [ ] **T-019** Build `ItemList` component — renders filtered items in a scrollable list; supports keyboard navigation (arrow keys to move focus); preserves scroll position when detail panel is open
- [ ] **T-020** Build `DetailPanel` component — slide-over panel from the right showing full item details, metadata, and action buttons (edit, delete, status change); arrow keys for next/prev item; Escape to close (US-0003)
- [ ] **T-021** Build `EmptyState` component — friendly illustration/message when filters return zero results; one-click "Reset filters" button; active filter count badge on filter bar (US-0004)
- [ ] **T-022** Configure Vite dev proxy (`vite.config.ts`) to forward `/api` requests from `:5173` to Express on `:3000`
