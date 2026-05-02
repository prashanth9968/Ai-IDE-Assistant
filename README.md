# 🤖 AI IDE Assistant

> A **VS Code extension** paired with a **Python/FastAPI backend** that delivers real-time AI-powered code completions for Java developers — powered by Microsoft's **CodeBERT** transformer model.

![Python](https://img.shields.io/badge/Python-3.10-3670A0?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-00C7B7?style=flat-square&logo=fastapi&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-Extension-007ACC?style=flat-square&logo=visualstudiocode&logoColor=white)
![HuggingFace](https://img.shields.io/badge/Model-CodeBERT-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📌 Overview

**AI IDE Assistant** integrates directly into VS Code and uses **Microsoft CodeBERT** — a transformer model pre-trained on millions of lines of code — to predict the next token as you write Java code. It reduces cognitive load and speeds up development by providing instant, context-aware suggestions.

```
You type Java code in VS Code
        ↓
Extension captures all code before your cursor
        ↓
Sends it to the local FastAPI backend (port 8000)
        ↓
CodeBERT predicts the next token using Masked LM
        ↓
Suggestion is inserted at your cursor position ✅
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 CodeBERT-powered | Transformer model trained on 6 programming languages |
| 🔍 Context-aware | Reads ALL code before the cursor — not just the current line |
| ⚡ On-demand | Triggered via VS Code Command Palette — no lag while typing |
| 🔌 REST API | Backend exposed as HTTP API — easily extensible to other editors |
| 🛡️ Error-resilient | Handles empty input, token limits, and backend failures gracefully |
| 📊 Progress UX | Shows a loading notification while fetching the suggestion |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────┐
│            VS Code Editor            │
│  ┌────────────────────────────────┐  │
│  │   TypeScript Extension         │  │
│  │   • Captures code before cursor│  │
│  │   • POST /complete → backend   │  │
│  │   • Inserts AI suggestion      │  │
│  └────────────┬───────────────────┘  │
└───────────────┼──────────────────────┘
                │  HTTP JSON  (localhost:8000)
┌───────────────▼──────────────────────┐
│          FastAPI Backend             │
│  ┌────────────────────────────────┐  │
│  │   CodeBERT (HuggingFace)       │  │
│  │   • Tokenise input code        │  │
│  │   • Append [MASK] token        │  │
│  │   • Predict top-1 token        │  │
│  │   • Return decoded completion  │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

---

## 🧰 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **ML Model** | [Microsoft CodeBERT](https://huggingface.co/microsoft/codebert-base) | Masked language modelling for code |
| **ML Framework** | PyTorch + HuggingFace Transformers | Model inference |
| **Backend** | Python 3.10, FastAPI, Uvicorn | REST API server |
| **Data Validation** | Pydantic v2 | Request/response schemas |
| **Frontend** | TypeScript, VS Code Extension API | Editor integration |
| **Build** | tsc (TypeScript compiler), npm | Extension compilation |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- VS Code 1.90+

### 1. Clone the Repo

```bash
git clone https://github.com/prashanth9968/Ai-IDE-Assistant.git
cd Ai-IDE-Assistant
```

### 2. Start the Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

> ⚠️ **First run:** CodeBERT (~500 MB) downloads automatically from HuggingFace. Subsequent runs use the local cache.

**Verify it's running:**
```bash
curl http://127.0.0.1:8000/
# → {"message":"AI IDE Assistant Backend Running","status":"ok"}
```

### 3. Build the VS Code Extension

```bash
cd vscode-extension
npm install
npm run compile
```

Press **F5** in VS Code to launch the Extension Development Host.

### 4. Use It

1. Open any `.java` file in VS Code
2. Place cursor where you want a suggestion
3. Press `Ctrl+Shift+P` → type **"Analyze Java Code"** → Enter
4. The AI-predicted token is inserted at your cursor ✅

---

## 📡 API Reference

### `GET /`
Health check.

```json
{ "message": "AI IDE Assistant Backend Running", "status": "ok" }
```

### `POST /complete`

**Request:**
```json
{
  "code": "public class HelloWorld { public static void main(String[] args) {"
}
```

**Response:**
```json
{
  "completion": " System"
}
```

**Error Responses:**

| Status | Reason |
|--------|--------|
| `400` | Empty code input |
| `422` | Tokenization failed |
| `500` | Internal model error |

---

## 📁 Project Structure

```
Ai-IDE-Assistant/
├── backend/
│   ├── main.py            # FastAPI app — CodeBERT inference logic
│   └── requirements.txt   # Pinned Python dependencies
├── vscode-extension/
│   ├── src/
│   │   └── extension.ts   # VS Code extension — command + API call
│   └── package.json       # Extension manifest
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions — backend health check CI
├── .gitignore
└── README.md
```

---

## 🔮 Roadmap

- [ ] Multi-token prediction (suggest full lines, not just one token)
- [ ] Support Python, JavaScript, and C++
- [ ] Fine-tune CodeBERT on a domain-specific Java dataset
- [ ] Inline ghost-text suggestions (like GitHub Copilot)
- [ ] VS Code Marketplace publish

---

## 👨‍💻 Author

**Naram Prashanth Goud**
Java Backend Developer · Spring Boot · DSA Enthusiast
📧 naramprashanthgoud@gmail.com · 🔗 [GitHub](https://github.com/prashanth9968)

---

## 📄 License

MIT License — feel free to use, modify, and distribute.
