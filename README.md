📄 DocMind

AI-powered Document Intelligence Platform

Turn raw documents into clear, actionable business intelligence using AI.

🚀 What is DocMind?

DocMind is a SaaS-style web application that helps people understand their documents using artificial intelligence.

Upload a file — get:

insights

summaries

risks

opportunities

action points

Instead of reading and analyzing documents manually, DocMind turns them into decision-ready intelligence.

🧠 What makes DocMind different?

Most “Chat with PDF” tools only answer questions.

DocMind acts like an AI consultant.

It doesn’t just summarize — it:

understands meaning

detects risks

highlights obligations

finds opportunities

creates structured reports

✨ AI Magic — Consulting-grade reports

DocMind includes a second-level AI system called AI Magic.

After a document is analyzed, the user can click ✨ Improve result, which launches a professional consultant-grade AI prompt that transforms raw analysis into a structured business report:

Executive Summary

Key Insights

Risks & Red Flags

Opportunities

Actionable Recommendations

TL;DR

This makes the output look like a human consultant’s report, not an AI response.

🪄 Features (MVP)

Upload PDF, TXT or DOCX

Choose analysis type:

Summary

Action items

Risks

Simple explanation

AI-powered document analysis (OpenRouter / OpenAI models)

AI Magic consulting report generation

PDF export of AI Magic reports

Built-in demo document

SaaS-style web interface

Document history per user

🧠 How it works

User logs in (no password, username only)

Uploads a document or uses the demo

Chooses an analysis type

AI analyzes the document

DocMind returns structured insights

User clicks ✨ Improve result to generate a professional report

The report can be downloaded as PDF

🎯 Who it’s for

DocMind is useful for:

Entrepreneurs & founders

Managers

Lawyers

Students

Anyone who works with documents and needs to understand them faster

🛠 Tech Stack

Backend: Python, FastAPI
Frontend: HTML, CSS, JavaScript, Tailwind
Database: SQLite
AI: OpenRouter API (e.g. OpenAI GPT-4o)
Document parsing: PyMuPDF, python-docx
Hosting: Render
CI/CD: GitHub

🔧 Setup & Run
Install dependencies
pip install -r requirements.txt

Environment variables

Copy .env.example to .env and set your OpenRouter key:
Get key → https://openrouter.ai/keys

OPENROUTER_API_KEY=sk-or-v1-...

Run the server
uvicorn backend.main:app --host 127.0.0.1 --port 8001

Open in browser
http://127.0.0.1:8001

📖 Usage Flow

Login — enter a name (no password required)

Dashboard — view uploaded documents

Upload — choose file and analysis type

Result — see AI analysis

AI Magic — generate consulting-grade report

Export — download PDF

📦 Project structure
/backend  
/frontend  
requirements.txt  
.env  
README.md  

⚠️ Disclaimer

This is a hackathon MVP built for demonstration purposes.
Not intended for production use.

🏆 Hackathon Project

Built to demonstrate:

AI document understanding

Business-grade AI reports

Real-world productivity value

SaaS-style product design