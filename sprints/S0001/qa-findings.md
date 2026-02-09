# QA Findings — Webview UI → Backend Integration & Invalid Input Handling

**Sprint:** S0001
**Date:** 2026-02-06
**Scope:** Verify the webview UI calls the backend correctly and handles invalid input.
**Method:** Static code review of `examples/webview-app/` (frontend + backend + shared schema).

---

## Test Plan

### Area 1 — UI → Backend API Calls

| # | Test Case | Frontend Entry Point | API Endpoint | Result |
|---|-----------|---------------------|-------------|--------|
| 1 | Initial page load fetches items | `loadItems()` on bootstrap (line 338) | `GET /api/v1/items` | PASS |
| 2 | Filter change reloads items | `change` listeners → `loadItems()` (lines 301-304) | `GET /api/v1/items?status=…&category=…` | PASS |
| 3 | Search input debounced reload | `input` → 300ms debounce → `loadItems()` (lines 305-308) | `GET /api/v1/items?search=…` | PASS |
| 4 | Pagination prev/next | Button clicks update `currentMeta.page` → `loadItems()` (lines 315-320) | `GET /api/v1/items?page=N` | PASS |
| 5 | Click item opens detail | `openDetail()` → `fetchItem(id)` (lines 215-230) | `GET /api/v1/items/:id` | PASS |
| 6 | Delete item calls API | `handleDelete()` → `deleteItem(id)` (lines 263-275) | `DELETE /api/v1/items/:id` | PASS |
| 7 | Clear/reset filters resets & reloads | `clearFilters()` → `loadItems()` (lines 252-259) | `GET /api/v1/items` (defaults) | PASS |
| 8 | Keyboard nav (arrows) opens detail | `navigateItem()` → `openDetail()` (lines 329-334) | `GET /api/v1/items/:id` | PASS |
| 9 | Request headers set Content-Type JSON | `apiFetch()` sets `Content-Type: application/json` (line 52) | All endpoints | PASS |
| 10 | 204 response handled (delete) | `apiFetch()` returns null on 204 (line 56) | `DELETE /api/v1/items/:id` | PASS |

### Area 2 — Invalid Input Handling

| # | Test Case | Frontend Behaviour | Backend Behaviour | Result |
|---|-----------|--------------------|--------------------|--------|
| 11 | API returns 400 validation error | `apiFetch()` throws structured Error with code/details (lines 60-64) | 400 + `VALIDATION_ERROR` envelope | PASS |
| 12 | List load failure shows error in UI | `loadItems()` catch renders `.error-message` div (lines 208-211) | N/A | PASS |
| 13 | Detail load failure feedback | `openDetail()` catch logs to console only (lines 227-229) | 404 `NOT_FOUND` | **FAIL** |
| 14 | Delete failure shows alert | `handleDelete()` catch calls `alert()` (lines 272-274) | 404/400 | PASS |
| 15 | Search maxlength enforced client-side | `<input maxlength="200">` (index.html line 50) | `validateQuery` checks ≤200 (validators.js line 149) | PASS |
| 16 | XSS prevention | `escapeHtml()` used for title/category rendering (lines 143, 147) | N/A | PASS |
| 17 | Invalid status in query params | Backend rejects with 400 | `validateQuery` checks enum (validators.js lines 137-146) | PASS |
| 18 | Invalid sort/order params | Backend rejects with 400 | `validateQuery` checks enum (validators.js lines 167-171) | PASS |
| 19 | Invalid page/pageSize params | Backend rejects with 400 | `validateQuery` checks integer + range (validators.js lines 159-164) | PASS |
| 20 | Non-JSON backend response | `res.json()` throws SyntaxError — unhandled gracefully | N/A | **FAIL** |
| 21 | Category filter not validated by backend | Unrecognized category returns empty list (no error) | No category enum validation in `validateQuery` | **WARN** |
| 22 | POST/PATCH body validation (title required) | N/A (no create/edit UI) | `validateBody` enforces required + length (validators.js lines 82-124) | PASS |

---

## Findings

### F-001 — Silent failure on item detail fetch (Medium)

**File:** `examples/webview-app/frontend/app.js` lines 224-229
**Severity:** Medium
**Category:** UX / Error handling

`openDetail()` catches fetch errors but only logs to `console.error`. The user receives no visible feedback when a detail fetch fails (e.g., item deleted by another user, network error). Compare with `loadItems()` which renders an inline error message, and `handleDelete()` which shows an `alert()`.

**Expected:** Display a user-visible error in the detail panel or a toast notification.
**Recommendation:** Render an error state inside `$detailPanel` or show an inline banner, consistent with the error handling in `loadItems()`.

---

### F-002 — Non-JSON error responses crash `apiFetch` (Medium)

**File:** `examples/webview-app/frontend/app.js` lines 49-68
**Severity:** Medium
**Category:** Robustness

`apiFetch()` unconditionally calls `res.json()` for all non-204 responses (line 58). If the backend returns a non-JSON response (e.g., an HTML proxy error page, a 502 from a reverse proxy, or a plain-text 500), `res.json()` will throw a `SyntaxError` instead of the structured error the callers expect.

**Expected:** Graceful handling of non-JSON responses with a fallback error message.
**Recommendation:** Wrap `res.json()` in a try/catch or check the `Content-Type` header before parsing.

---

### F-003 — No loading/spinner state during API calls (Low)

**File:** `examples/webview-app/frontend/app.js`
**Severity:** Low
**Category:** UX

No loading indicator is shown during any API call (`loadItems`, `openDetail`, `handleDelete`). On slow connections or when the backend is unresponsive, the UI appears frozen with no feedback.

**Expected:** A spinner or skeleton state while data is loading.

---

### F-004 — Category filter values not validated on backend (Low)

**File:** `examples/webview-app/backend/validators.js` lines 132-185
**Severity:** Low
**Category:** Validation gap

`validateQuery` validates `status` against the schema enum but does not validate the `category` query parameter against any allow-list. An arbitrary category value like `?category=XSS_ATTEMPT` would simply produce an empty result set (no crash), so this is low-severity. However, it is inconsistent with the `status` validation approach.

---

### F-005 — Soft-delete confirmation implies restorability but no restore UI exists (Low)

**File:** `examples/webview-app/frontend/app.js` line 265
**Severity:** Low
**Category:** UX

The delete confirmation says _"This action is reversible (soft delete)"_, which is technically true at the data layer. However, no UI exists to undelete items, making this effectively irreversible from the user's perspective.

---

## Verdict

| Severity | Count |
|----------|-------|
| Medium   | 2 (F-001, F-002) |
| Low      | 3 (F-003, F-004, F-005) |

**Overall:** The UI correctly calls all documented backend endpoints. Filter, search, pagination, detail, and delete flows all route to the correct API paths with proper parameters. Backend validation is solid with structured error envelopes. Two medium-severity gaps exist in frontend error handling that should be addressed before release: silent detail fetch failures (F-001) and non-JSON response handling (F-002). No critical/blocking defects found.
