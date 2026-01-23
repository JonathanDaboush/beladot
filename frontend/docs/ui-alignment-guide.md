# UI Alignment & Components Guide

This guide outlines how users see the frontend and how core components compose together across the app. The `/ui` route provides an interactive showcase with mock data.

## Layout & Structure
- Global wrapper: `Layout` renders the `Header`, role-based redirect, and the main content area.
- Max widths: Use `.page` for centered content with comfortable margins and `.section` to separate vertical blocks.
- Grid system: Use Bootstrap rows/cols (`.row .col-*`) for responsive alignment; prefer `g-3`/`g-4` for spacing.
- Theme: Colors, spacing, and common utilities live in `src/styles/theme.css`. Keep spacing consistent with existing variables and helpers.

## Navigation
- `Header` adapts by route prefix via `usePortalType` (user, employee, seller). It shows:
  - User portal: logo, search, categories with subcategory hover.
  - Employee/Seller portals: title indicator + `UserMenu` on the right.
- `RoleBasedRedirect` (inside `Layout`) enforces appropriate portal access rules.

## Catalog → Detail Flow
- `CatalogPage`: paginated grid; parent supplies `items`, `onItemClick`, and a `renderSummary(item)` card.
- `DetailPage`: images, variants, description, rating, and reviews. Parent manages `selectedVariant` and `onVariantChange`.
- Use bootstrap utility classes for alignment: `container`, `row`, `col-*`, `align-items-center`, `gap-*`.

## Components
- `InfoBox`: compact feature highlights (e.g., Free Shipping) used in rows or sidebars.
- `Reviews`: list with timestamps; optional seller response nests below the review.
- `OrderAddressForm`: controlled form with `onChange` callback. Align in a two-column layout with a live preview when needed.

## Showcase
- Visit `/ui` to see:
  - A paginated catalog grid with sample products
  - A product detail view with images, variants, and reviews
  - Info boxes row
  - Order address form with live JSON preview

## Alignment Rules of Thumb
- Keep vertical rhythm: place sections within `.section` and avoid ad-hoc margins.
- Card content: pad with `.product-body` and keep headings compact.
- Imagery: use fixed aspect ratios (`aspect-ratio` in theme.css) to avoid layout shift.
- Hover & focus: respect theme colors; keep shadows subtle (`.shadow-soft`).

## Extending
- Add more examples to `/ui` as new components arrive (cart, checkout, finance dashboards).
- When creating new pages, wrap content in `.page` and group blocks with `.section` for consistent spacing.
