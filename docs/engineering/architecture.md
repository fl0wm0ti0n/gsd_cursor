# Architecture

## Overview

The application follows a **frontend + backend split** with a clear API boundary. Both layers use TypeScript to enable shared type definitions and validation schemas across the stack.

```
┌──────────────────────────────────────────────────┐
│                   Frontend (SPA)                 │
│  React 18 · TypeScript · Vite · TanStack Query   │
│                                                  │
│  ┌────────────┐  ┌──────────┐  ┌──────────────┐ │
│  │ Filter Bar │  │ List View│  │ Detail Panel │ │
│  └─────┬──────┘  └────┬─────┘  └──────┬───────┘ │
│        └───────────────┴───────────────┘         │
│                        │ HTTP/JSON                │
└────────────────────────┼─────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │          API Gateway           │
         │   Express · TypeScript · Zod   │
         ├───────────────────────────────┤
         │   Routes → Validators → Svc   │
         └───────────────┬───────────────┘
                         │
              ┌──────────┴──────────┐
              │      Data Layer     │
              │  SQLite (dev/test)  │
              │  PostgreSQL (prod)  │
              └─────────────────────┘
```

## Components

### Frontend (`/frontend`)

| Concern | Choice | Rationale |
|---------|--------|-----------|
| Framework | React 18 | Component model fits filter bar, list, and panel UX |
| Build | Vite | Fast HMR, native TS support |
| State / data fetching | TanStack Query | Cache-first fetching, optimistic updates for detail panel (US-0003) |
| Routing | React Router v6 | Filter state persisted in URL search params (answers PO open question) |
| Styling | Tailwind CSS | Utility-first, fast iteration on chip/filter UI |

Key modules:

- `components/FilterBar.tsx` — chip-based multi-select filters (US-0002)
- `components/ItemList.tsx` — virtualized list with keyboard nav
- `components/DetailPanel.tsx` — slide-over panel, arrow-key traversal (US-0003)
- `components/EmptyState.tsx` — friendly empty state with reset action (US-0004)
- `hooks/useFilters.ts` — reads/writes filter state to URL search params
- `api/client.ts` — typed API client generated from shared schema

### Backend (`/backend`)

| Concern | Choice | Rationale |
|---------|--------|-----------|
| Runtime | Node.js 20 LTS | Matches frontend language (TypeScript) |
| Framework | Express 5 | Minimal, well-understood, large middleware ecosystem |
| Validation | Zod 3 | Shared schemas with frontend; generates OpenAPI |
| ORM | Drizzle ORM | Lightweight, type-safe, supports SQLite + PostgreSQL |
| API spec | OpenAPI 3.1 (auto-generated from Zod via `zod-to-openapi`) | Single source of truth |

Key modules:

- `routes/items.ts` — CRUD + filtered list endpoint
- `middleware/validate.ts` — generic Zod validation middleware
- `services/item.service.ts` — business logic
- `db/schema.ts` — Drizzle table definitions

### Shared (`/shared`)

A small package consumed by both frontend and backend (via TypeScript path aliases or a workspace package):

- `schemas/item.schema.ts` — Zod schemas for Item create/update/filter
- `schemas/filter.schema.ts` — Zod schema for filter query params
- `types/` — inferred TypeScript types (`z.infer<typeof ...>`)

## API Schema

### Base URL

`/api/v1`

### Endpoints

#### `GET /items`

Returns a filtered, paginated list of items.

**Query parameters** (all optional):

| Param | Type | Description |
|-------|------|-------------|
| `status` | `string[]` | Filter by status (comma-separated) |
| `category` | `string[]` | Filter by category (comma-separated) |
| `dateFrom` | `ISO 8601 string` | Items created on or after |
| `dateTo` | `ISO 8601 string` | Items created on or before |
| `search` | `string` | Free-text search |
| `page` | `integer ≥ 1` | Page number (default 1) |
| `pageSize` | `integer 1–100` | Items per page (default 25) |
| `sort` | `string` | Sort field (e.g. `createdAt`, `title`) |
| `order` | `asc \| desc` | Sort direction (default `desc`) |

**Response `200`:**

```json
{
  "data": [
    {
      "id": "uuid",
      "title": "string",
      "status": "open | in_progress | done",
      "category": "string",
      "description": "string",
      "createdAt": "ISO 8601",
      "updatedAt": "ISO 8601"
    }
  ],
  "meta": {
    "page": 1,
    "pageSize": 25,
    "totalItems": 142,
    "totalPages": 6,
    "activeFilters": 2
  }
}
```

#### `GET /items/:id`

Returns a single item with full details (used by the detail panel).

**Response `200`:**

```json
{
  "data": {
    "id": "uuid",
    "title": "string",
    "status": "open | in_progress | done",
    "category": "string",
    "description": "string",
    "metadata": {},
    "createdAt": "ISO 8601",
    "updatedAt": "ISO 8601"
  }
}
```

**Response `404`:** `{ "error": { "code": "NOT_FOUND", "message": "Item not found" } }`

#### `POST /items`

Creates a new item.

**Request body:**

```json
{
  "title": "string (1–200 chars, required)",
  "status": "open | in_progress | done (default: open)",
  "category": "string (1–100 chars, required)",
  "description": "string (max 5000 chars, optional)"
}
```

**Response `201`:** Full item object.

#### `PATCH /items/:id`

Partial update. Same fields as POST, all optional. Returns updated item.

#### `DELETE /items/:id`

Soft-delete. Returns `204 No Content`.

### Error envelope

All errors follow a consistent shape:

```json
{
  "error": {
    "code": "VALIDATION_ERROR | NOT_FOUND | INTERNAL_ERROR",
    "message": "Human-readable message",
    "details": []
  }
}
```

For validation errors, `details` contains per-field issues:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      { "field": "title", "message": "Required" },
      { "field": "pageSize", "message": "Must be between 1 and 100" }
    ]
  }
}
```

## Validation Strategy

### Principle: Single schema, both sides

Zod schemas defined in `/shared` are the **single source of truth** for validation. They are consumed in three places:

1. **Backend middleware** — `validate.ts` parses `req.query`, `req.body`, and `req.params` before the handler runs. Invalid requests receive a `400` with structured error details.
2. **Frontend forms** — The same Zod schemas integrate with React Hook Form via `@hookform/resolvers/zod` for inline field validation.
3. **API client** — Response data is parsed through Zod schemas on the frontend to catch contract drift at runtime.

### Schema example (shared)

```typescript
// shared/schemas/item.schema.ts
import { z } from "zod";

export const ItemStatus = z.enum(["open", "in_progress", "done"]);

export const CreateItemSchema = z.object({
  title: z.string().min(1).max(200),
  status: ItemStatus.default("open"),
  category: z.string().min(1).max(100),
  description: z.string().max(5000).optional(),
});

export const UpdateItemSchema = CreateItemSchema.partial();

export const ItemFilterSchema = z.object({
  status: z.array(ItemStatus).optional(),
  category: z.array(z.string()).optional(),
  dateFrom: z.string().datetime().optional(),
  dateTo: z.string().datetime().optional(),
  search: z.string().max(200).optional(),
  page: z.coerce.number().int().min(1).default(1),
  pageSize: z.coerce.number().int().min(1).max(100).default(25),
  sort: z.enum(["createdAt", "updatedAt", "title"]).default("createdAt"),
  order: z.enum(["asc", "desc"]).default("desc"),
});

export type CreateItem = z.infer<typeof CreateItemSchema>;
export type UpdateItem = z.infer<typeof UpdateItemSchema>;
export type ItemFilter = z.infer<typeof ItemFilterSchema>;
```

### Backend validation middleware

```typescript
// backend/middleware/validate.ts
import { ZodSchema } from "zod";
import { Request, Response, NextFunction } from "express";

export function validate(target: "body" | "query" | "params", schema: ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req[target]);
    if (!result.success) {
      return res.status(400).json({
        error: {
          code: "VALIDATION_ERROR",
          message: "Request validation failed",
          details: result.error.issues.map((i) => ({
            field: i.path.join("."),
            message: i.message,
          })),
        },
      });
    }
    req[target] = result.data; // Replace with parsed/coerced values
    next();
  };
}
```

### Frontend form integration

```typescript
// frontend/components/CreateItemForm.tsx (sketch)
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { CreateItemSchema, CreateItem } from "@shared/schemas/item.schema";

function CreateItemForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<CreateItem>({
    resolver: zodResolver(CreateItemSchema),
  });
  // ...
}
```

### OpenAPI generation

```typescript
// backend/openapi.ts
import { OpenAPIRegistry } from "@asteasolutions/zod-to-openapi";
import { CreateItemSchema, ItemFilterSchema } from "@shared/schemas/item.schema";

const registry = new OpenAPIRegistry();
registry.registerPath({
  method: "get",
  path: "/api/v1/items",
  request: { query: ItemFilterSchema },
  // ...
});
// Export as JSON/YAML for docs or client codegen.
```

## Folder Structure

```
/
├── frontend/               # React SPA
│   ├── src/
│   │   ├── api/            # Typed API client
│   │   ├── components/     # UI components
│   │   ├── hooks/          # Custom hooks (useFilters, etc.)
│   │   ├── pages/          # Route-level components
│   │   └── main.tsx
│   ├── index.html
│   ├── vite.config.ts
│   └── package.json
├── backend/                # Express API
│   ├── src/
│   │   ├── routes/         # Route handlers
│   │   ├── middleware/      # validate, auth, error handler
│   │   ├── services/       # Business logic
│   │   ├── db/             # Drizzle schema + migrations
│   │   └── server.ts
│   └── package.json
├── shared/                 # Shared Zod schemas + types
│   ├── schemas/
│   ├── types/
│   └── package.json
├── package.json            # Workspace root (npm workspaces)
└── tsconfig.base.json      # Shared TS config
```

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Shared schema drift (FE/BE versions diverge) | Medium | High | Single `/shared` workspace package; CI verifies both build against same version |
| SQLite → PostgreSQL migration pain | Low | Medium | Drizzle abstracts dialect; integration tests run against both |
| Filter query params exceed URL length limit | Low | Low | Compress with base64 encoding if >2k chars; add POST-based filter endpoint as fallback |
| Optimistic update conflicts in detail panel | Medium | Medium | TanStack Query mutation with rollback; backend returns updated `updatedAt` for conflict detection |

## Decisions

- [DEC-0001](../../decisions/DEC-0001.md) — Frontend/backend technology split
- [DEC-0002](../../decisions/DEC-0002.md) — Validation strategy: shared Zod schemas
