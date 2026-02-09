# Vision

## Problem
- ...

## Audience
- ...

## Value
- ...

## Look and Feel
- ...

## UX References

### 1. Airbnb — Filter Bar + Instant Results
- **Source:** airbnb.com search experience
- **Pattern:** Horizontal filter chips (price, type, amenities) sit above results. Selecting a filter instantly refines the list without a full page reload. Active filters are visually highlighted as filled chips with an "×" to remove.
- **Takeaway:** Filters should feel lightweight and reversible. Users see the effect immediately, encouraging exploration rather than committing to a search upfront.

### 2. Linear — Side-Panel Detail View
- **Source:** linear.app issue tracker
- **Pattern:** Clicking an item in the list opens a slide-over detail panel on the right while the list remains visible and scrollable on the left. The detail panel contains all metadata, comments, and actions. Pressing Escape or clicking outside closes the panel and returns focus to the list.
- **Takeaway:** A non-navigating detail view preserves list context and supports rapid scanning. Users can review multiple items without losing their place.

### 3. Notion Database — Multi-Select Faceted Filters
- **Source:** notion.so database views
- **Pattern:** A "Filter" button opens a dropdown builder where users add conditions (e.g., Status is "In Progress", Tag contains "UX"). Multiple conditions stack with AND/OR logic. A small badge on the Filter button shows the active filter count.
- **Takeaway:** For power users, composable filter rules offer precision. The badge count provides at-a-glance awareness that results are filtered, reducing surprise.

## Intended Interaction Flow — Filters & Details

### Filter Flow
1. **Default state:** All items are visible; no filters are active. The filter bar shows available dimensions (e.g., status, category, date range) as collapsed chips or buttons.
2. **Activate filter:** User clicks a filter chip -> a small popover/dropdown appears with selectable options (checkboxes for multi-select, radio for single-select). Selecting an option immediately updates the result list.
3. **Stack filters:** Multiple filters can be active simultaneously (AND logic). Each active filter shows as a filled chip with an "×" dismiss control. A "Clear all" link appears when 2+ filters are active.
4. **Empty state:** If the active filters produce zero results, show a friendly empty state with a suggestion to relax filters or a one-click "Reset filters" button.

### Detail Flow
1. **Trigger:** User clicks a list item (row or card).
2. **Panel opens:** A detail panel slides in from the right (or expands inline on narrow viewports). The list remains visible but dims or narrows to accommodate the panel.
3. **Content:** The panel displays full metadata, descriptions, related items, and action buttons (edit, delete, status change).
4. **Navigation:** Arrow keys or swipe gestures allow moving to the next/previous item without closing the panel.
5. **Close:** Pressing Escape, clicking the "×" button, or clicking the dimmed list area closes the panel and restores the full list view.

