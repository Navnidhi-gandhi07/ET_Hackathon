
Problem Statement -2 Agentic AI for Autonomous Enterprise Workflows
Design a multi-agent system that takes ownership of a complex, multi-step enterprise process. It should 
detect failures, self-correct, and complete the job with minimal human involvement — while keeping an 
auditable trail of every decision it makes. 
# 🚆 Sanchaalan — Agentic AI Document Intelligence System

Sanchaalan is an end-to-end multi-agent AI system designed to automate document-driven enterprise workflows. It processes documents, extracts insights, generates role-based outputs, assigns priorities, and triggers actions — with minimal human intervention and full traceability.

This project demonstrates a real-world railway operations use case while remaining applicable to general enterprise workflows.

---

## 🚀 What the System Does

- Upload documents (PDF, DOCX, EML)
- Extract text, tables, and images (OCR supported)
- Generate role-based summaries:
  - Engineering
  - Finance
  - Safety
  - HR
  - Management
- Export summaries as DOCX snapshots
- Automatically trigger alerts (email)
- Allow users to ask questions on documents (Q&A)
- Provide answers strictly from document content with citations

---

## 🤖 Multi-Agent Workflow

The system uses multiple agents:

- Planner Agent → defines workflow
- Retrieval Agent → fetches relevant content
- Decision Agent → assigns priority
- Action Agent → triggers alerts (email)
- Verification Agent → ensures correctness

Includes:
- Autonomous execution of multiple steps
- Error detection and retry
- Decision logging for auditability

---

## 🏗️ Architecture (Flow)

Ingestion → Processing (OCR + Parsing + Chunking) → Agent Layer → Storage →  
Summarization (Role-based snapshots) → Decision Engine → Alerts → Query Layer (RAG)

---

## 📁 Project Structure

Sanchaalan/
- app.py (Flask backend)
- mvp.py (processing + agents)
- smtp.py (email)
- frontend/ (React UI)
- uploads/
- snapshots_out/
- logs/

---

# ⚙️ Setup & Run (Windows)

## 1. Clone Repo

```bash
git clone https://github.com/Navnidhi-gandhi07/ET_Hackathon.git
cd ET_Hackathon
```

---

## 2. Backend Setup

```bash
python -m venv venv
venv\Scripts\activate

pip install flask flask-cors werkzeug python-dotenv
pip install pymupdf pdfplumber pillow pytesseract langdetect
pip install transformers torch sentencepiece python-docx
```

---

## 3. Install Tesseract OCR

Download:
https://github.com/UB-Mannheim/tesseract/wiki

Add to PATH:
C:\Program Files\Tesseract-OCR\

Verify:
```bash
tesseract --version
```

---

## 4. Setup Email (Optional)

Create `.env` file:

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
SMTP_FROM=your_email@gmail.com
```

---

## 5. Run Backend

```bash
python app.py
```

Runs at:
http://localhost:5000

---

## 6. Frontend Setup

```bash
cd frontend
npm install
npm install axios bootstrap
npm start
```

Runs at:
http://localhost:3000

---

# 🌐 How to Use

1. Open browser → http://localhost:3000  
2. Upload a document  
3. System processes it automatically  
4. Download role-based snapshots  
5. Ask questions using the query box  
6. Get answers with confidence + citations  

---

# 📊 Impact

- 60–70% reduction in manual effort  
- 2–3x faster decision-making  
- Improved coordination across teams  
- Faster response to critical issues  

---

# 🧠 Summary

Sanchaalan converts unstructured documents into:

- Actionable insights  
- Role-specific outputs  
- Automated decisions  

— enabling autonomous and traceable enterprise workflows.

---

## 👨‍💻 Author

Built as a solo project for Agentic AI workflow automation.
