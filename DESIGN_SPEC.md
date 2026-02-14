# DocMind UI & UX Design Specification

## 1. Product positioning
DocMind is a premium SaaS product for AI-powered document analysis.
It should visually feel like:
- Notion
- Linear
- Stripe
- Vercel
- OpenAI

The interface must feel:
- Clean
- Calm
- Minimal
- Professional
- Trustworthy

Target audience:
Business users, lawyers, managers, consultants, startup founders.

The design must feel like a product people trust with important documents.

---

## 2. Visual style

Use Tailwind CSS.

Style guidelines:
- Light background (white / gray-50)
- Cards on white with soft shadow
- Rounded corners
- Generous spacing
- No clutter
- No bright colors
- Blue as primary accent

Primary color:
Blue-500

Background:
Gray-50

Text:
Gray-900 (headings)
Gray-600 (body)

---

## 3. UX Principles

The user journey must feel:
- Simple
- Calm
- Guided
- Never overwhelming

The user should always know:
- What they uploaded
- What the AI is doing
- What they got back

Use:
- Step-based flow
- Clear buttons
- Empty states
- Loading states

---

## 4. Screens to implement

The following screens must be visually redesigned:

1) Login
2) Dashboard
3) Upload Document
4) Choose Analysis Type
5) Analysis Result

All screens should:
- Look consistent
- Share the same style
- Use cards
- Use spacing
- Feel like a modern SaaS

---

## 5. UI Components

Use these components everywhere:
- Card containers
- Primary buttons
- Secondary buttons
- Tables
- File upload area
- Loading indicators
- Result boxes

All UI must be built using:
- HTML
- Tailwind CSS

Do NOT use React or frontend frameworks.

---

## 6. Quality bar

This design should be good enough that:
If shown on Product Hunt, people would believe this is a real startup.

Avoid:
- ugly layouts
- default browser styles
- cramped elements
- raw HTML look

---

## 7. Implementation approach

Cursor should:
1. Create or update HTML templates
2. Apply Tailwind styles
3. Ensure consistency across pages
4. Make the UI look like a polished SaaS
5. Keep all existing functionality working

Do not break backend or API.
Only improve the frontend.
