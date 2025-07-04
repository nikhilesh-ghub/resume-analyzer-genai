# 🧠 AI-Powered Resume Analyzer using Generative AI (Gemini + LangChain)

This project is an AI-powered resume analyzer that leverages **Google Gemini**, **LangChain**, and **Gradio** to extract skills, experience, education, and keywords from resumes and job descriptions. It performs a **skill gap analysis**, generates a **job-fit score**, and even creates a **tailored cover letter**.

---



## 🚀 Features

- 📄 Upload your **resume** and a **job description** (PDF or TXT)
- 🔍 Extract key sections using **LLM-based NLP**
- ⚖️ Get a **skill gap analysis**
- 📊 See a **job-fit score** (0–100)
- ✍️ Receive resume **improvement suggestions**
- 💌 Generate a **custom cover letter**
- 🌐 Gradio-based UI for easy use

---



## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| 🧠 LangChain | LLM orchestration |
| 🌐 Google Gemini API | Generative AI |
| 🎨 Gradio | Web UI |
| 📄 pdfminer.six | PDF Text Extraction |
| 🐍 Python | Core Logic |
| 🔐 python-dotenv | Secure API Management |

---
## 🌐 API Usage

This project uses the **Google Gemini API** via the [LangChain](https://www.langchain.com/) framework to power all LLM-based text extraction and generation.

- **API Used**: `Google Generative AI (Gemini 1.5 via langchain-google-genai)`
- **Functionality Powered by API**:
  - Extracting structured information (skills, experience, education, keywords)
  - Generating resume improvement suggestions
  - Creating a customized cover letter
- **Authentication**: Requires `GOOGLE_API_KEY` stored securely in a `.env` file
- **Integration Framework**: LangChain



---

---

## 📦 Installation

### 🔧 Prerequisites
- Python 3.8+
- A Google Gemini API key

### 📥 Clone and Install

```bash
git clone https://github.com/your-username/resume-analyzer-genai.git
cd resume-analyzer-genai
pip install -r requirements.txt


