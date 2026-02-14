AI Magic Screen — Product Spec

Goal:
Turn raw document analysis into a human-friendly, business-grade AI report.

User flow:

User uploads document

AI analysis runs

User clicks “✨ AI Magic”

Backend calls LLM with analysis

AI returns structured consulting-style report

UI renders formatted AI Magic screen

Output sections:

Executive Summary

Key Insights

Risks & Red Flags

Opportunities

Actionable Recommendations

TL;DR

Backend:

New endpoint POST /ai/magic

Input: document_id

Uses existing OpenAI client

Prompt style: “You are an AI consultant…”

Frontend:

New button on analysis result page

New AI Magic screen

Loading animation

Clean card-style layout