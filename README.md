DocMind 🧠📄

AI-powered document intelligence platform

DocMind is a SaaS-style web application that helps people understand their documents using artificial intelligence.

Upload a file — get clear insights, summaries, risks, opportunities, and action points.

🚀 What is DocMind?

People deal with contracts, reports, lectures, and documents every day — but reading and analyzing them takes time and mental effort.

DocMind uses AI to:

Understand the meaning of a document

Extract the most important information

Highlight risks, obligations, and red flags

Reveal opportunities

Turn raw text into clear, actionable insights

Unlike simple “chat with PDF” tools, DocMind transforms documents into decision-ready intelligence.

🪄 AI Magic — Consulting-grade reports

DocMind includes a second-level AI system called AI Magic.

After a document is analyzed, the user can click ✨ Improve result, which launches a professional AI consultant prompt that converts raw analysis into a structured business-grade report:

Executive Summary

Key Insights

Risks & Red Flags

Opportunities

Actionable Recommendations

TL;DR

This turns an AI response into something that looks like a report from a human consultant.

✨ Features (MVP)

Upload PDF, TXT or DOCX documents

Choose how to analyze:

Summary

Action items

Risks

Simple explanation

AI-powered document analysis (OpenRouter / OpenAI models)

AI Magic consulting report generation

PDF export of AI Magic reports

Built-in Demo Document for instant testing

SaaS-style web interface

Document history per user

🧠 How it works

User logs in with a username

Uploads a document (or uses the demo file)

Chooses an analysis type

DocMind sends the document to AI

AI returns structured insights

User can click ✨ Improve result to get a consulting-grade AI report

The report can be downloaded as PDF

🎯 Who this is for

DocMind is useful for:

Entrepreneurs and founders

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

Cloud hosting: Render

CI/CD: GitHub

🔧 Setup and run

Install dependencies
From project root:

pip install -r requirements.txt


Environment variables
Copy .env.example to .env and set your OpenRouter key:

Get key: https://openrouter.ai/keys

In .env:

OPENROUTER_API_KEY=sk-or-v1-...


Run the server
From project root:

uvicorn backend.main:app --host 127.0.0.1 --port 8001


Open in browser
http://127.0.0.1:8001

📖 Usage flow

Login — enter a name on the homepage (no password required).

Dashboard — see uploaded documents and the “Upload” button.

Upload — choose a file and analysis type, then click “Analyze”.

Result — view the AI analysis.

AI Magic — click ✨ Improve result to generate a professional report.

Export — download the AI Magic report as PDF.

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

Built for an AI-powered application hackathon to demonstrate:

AI document understanding

Business-grade AI reports

Real-world productivity value

SaaS-style product design