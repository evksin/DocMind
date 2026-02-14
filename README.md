# DocMind 🧠📄  
**AI-powered document analysis**

DocMind is a SaaS-style web application that helps people understand their documents using artificial intelligence.

Upload a file — get clear insights, summaries, risks, and action points.

---

## 🚀 What is DocMind?

People deal with contracts, reports, lectures, and documents every day — but reading and analyzing them takes time.

DocMind uses AI to:
- Understand the meaning of a document
- Extract the most important information
- Highlight risks and obligations
- Turn text into clear, actionable insights

---

## ✨ Features (MVP)

- Upload PDF or TXT documents  
- Choose how to analyze:
  - Summary  
  - Action items  
  - Risks  
  - Simple explanation  
- AI-powered analysis via OpenRouter (OpenAI and other models)  
- SaaS-style web interface  
- Document history per user  

---

## 🧠 How it works

1. User logs in with a username  
2. Uploads a document  
3. Chooses an analysis type  
4. DocMind sends the text to AI  
5. AI returns structured insights  
6. User sees and saves the result  

---

## 🛠 Tech Stack

- **Backend:** Python, FastAPI  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** SQLite  
- **AI:** OpenRouter API (e.g. OpenAI GPT-4o)  
- **Document parsing:** PyMuPDF, python-docx  

---

## 🔧 Setup and run

1. **Установка зависимостей**  
   Из корня проекта:
   ```powershell
   pip install -r requirements.txt
   ```

2. **Переменные окружения**  
   Скопируйте `.env.example` в `.env` и укажите ключ OpenRouter:
   - Ключ: [openrouter.ai/keys](https://openrouter.ai/keys)
   - В `.env`: `OPENROUTER_API_KEY=sk-or-v1-...`

3. **Запуск**  
   Из корня проекта запустите бэкенд (он же раздаёт фронтенд):
   ```powershell
   uvicorn backend.main:app --host 127.0.0.1 --port 8001
   ```

4. **Открыть в браузере**  
   [http://127.0.0.1:8001](http://127.0.0.1:8001)

---

## 📖 Сценарий использования

1. **Вход** — на главной введите имя и нажмите «Войти» (пароль не требуется).
2. **Дашборд** — отображаются ваши загруженные документы, ссылка «Загрузить документ».
3. **Загрузка** — выберите файл (PDF, TXT или DOCX), тип анализа (краткое изложение, действия, риски, объяснение простыми словами), нажмите «Анализировать».
4. **Результат** — отображается ответ ИИ; кнопка «Назад к дашборду» возвращает к списку документов.

---

## 📦 Project structure

/backend
/frontend
requirements.txt
.env
README.md

---

## ⚠️ Disclaimer

This is a hackathon MVP built for demonstration purposes.
Not intended for production use.

---

## 🏆 Hackathon Project

Built for an AI-powered application hackathon to demonstrate:
- AI document understanding
- Real-world business value
- SaaS-style product design
