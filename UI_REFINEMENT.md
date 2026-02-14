# DocMind UI Refinement Specification

## Goal
Transform the current UI from a simple admin-like interface into a premium SaaS product.

The UI must feel:
- Clean
- Calm
- Professional
- Trustworthy
- Like a real startup product (Notion, Linear, OpenAI style)

---

## 1. Layout & spacing

All pages must:
- Use max-width container (max-w-5xl or max-w-4xl)
- Be centered using mx-auto
- Have horizontal padding (px-6 or px-8)
- Have vertical spacing (py-8 or py-10)

The content must not stretch across the full screen.

---

## 2. Page background

All pages should use:
- bg-gray-50

All content blocks must be:
- bg-white
- rounded-xl
- shadow-sm or shadow-lg

This creates depth and a layered SaaS feel.

---

## 3. Header (top bar)

The top bar must:
- Have a bottom border
- Contain:
  - Product name: DocMind
  - Subtitle: "AI Document Intelligence"
  - User info on the right

The header should feel like a real SaaS navigation bar.

---

## 4. Typography

Use Tailwind text styles:
- Main titles: text-2xl font-semibold text-gray-900
- Section titles: text-lg font-medium
- Body text: text-gray-600
- Metadata (dates, etc): text-sm text-gray-400

---

## 5. Document list

Each document row should be converted into a card:
- bg-white
- rounded-xl
- shadow-sm
- hover:shadow-md
- transition

Inside each card:
- File name (bold)
- Date (small gray text)
- Actions on the right

---

## 6. Buttons

Primary buttons:
- bg-blue-600
- hover:bg-blue-700
- text-white
- font-medium
- px-5 py-2.5
- rounded-lg
- shadow

Secondary buttons:
- text-blue-600
- hover:text-blue-800

Delete buttons:
- text-red-500
- hover:text-red-700

---

## 7. Empty space

Avoid large empty areas.

Use:
- max-w containers
- spacing between elements (space-y-4, space-y-6)

The UI should feel compact but breathable.

---

## 8. Quality bar

The result should look like:
A product that could be shown on Product Hunt and not be laughed at.

No raw HTML look.
No default browser styles.
No ugly tables.
No cramped UI.

---

## 9. Implementation rules

- Do not break backend or functionality
- Only change HTML and Tailwind classes
- Apply changes consistently across all pages
