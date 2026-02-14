# DocMind — AI Document Analyst (Hackathon MVP)

## Project goal
DocMind is a SaaS-style web application that allows users to upload documents and analyze them using AI.

The goal is to turn complex, unstructured files (PDF, TXT, DOCX) into clear, useful, and structured information such as summaries, risks, and action items.

This is a hackathon MVP, not a production system. The focus is clarity, usability, and a working AI-powered product.

---

## Core user flow

1. User enters a username (simple login, no password).
2. User sees a dashboard with previously uploaded documents.
3. User uploads a new document (PDF or TXT).
4. User selects an analysis type:
   - Summary
   - Action Items
   - Risks
   - Explain in simple words
5. The system sends the document text + selected action to OpenAI.
6. The AI returns a structured response.
7. The user sees the result and can return to the dashboard.

---

## MVP Features

- Web-based interface (no installation).
- Simple SaaS-style layout:
  - Login
  - Dashboard
  - Upload page
  - Results page
- File upload and text extraction.
- AI-powered document analysis.
- History of documents and results per user.

---

## Tech stack

### Frontend
- HTML
- CSS
- Vanilla JavaScript
- Fetch API for backend calls

### Backend
- Python
- FastAPI
- Uvicorn

### Database
- SQLite
- SQLAlchemy or simple SQLite integration

Tables:
- users
- documents
- results

### Document processing
- PDF: PyMuPDF or pdfplumber
- TXT: built-in Python
- DOCX (optional): python-docx

### AI
- OpenAI API (GPT-4 or GPT-4o)
- Prompt templates for each analysis type

---

## Architecture

Browser (Frontend)
→ FastAPI Backend
→ Document Parser
→ OpenAI API
→ Response
→ Frontend

---

## AI behavior

The AI must:
- Read the full document text.
- Follow the selected action (summary, risks, etc).
- Produce short, clear, structured output.
- Use simple, non-technical language.

---

## Project structure

- /backend
- /frontend
- requirements.txt
- .env (OpenAI key)
- README.md

---

## Constraints

- Keep everything simple.
- No real authentication.
- No payments.
- No complex UI frameworks.
- Focus on reliability and clarity.
