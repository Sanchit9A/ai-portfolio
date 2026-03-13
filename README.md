# 🤖 Sanchit's AI Portfolio

> Building real AI applications with Python, LangChain, Groq and Streamlit

![Python](https://img.shields.io/badge/Python-3.12-blue)
![LangChain](https://img.shields.io/badge/LangChain-1.2.12-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![Groq](https://img.shields.io/badge/Groq-Free%20LLM-orange)

---

## 🚀 Projects

### 1️⃣ NewsBot — Ask Your Articles
> Ask questions from any news article using RAG!

**What it does:**
- Paste 1-3 news article URLs
- Ask any question
- AI finds relevant content and answers!

**Live Demo:** [Coming Soon]
**Tech Stack:** LangChain · FAISS · HuggingFace · Groq · Streamlit

---

### 2️⃣ AI Tools Agent
> AI that thinks and uses tools to answer anything!

**What it does:**
- Ask any question
- AI decides which tool to use
- Wikipedia / Web Search / Calculator

**Live Demo:** [Coming Soon]
**Tech Stack:** LangGraph · Groq · DuckDuckGo · Wikipedia · Streamlit

---

### 3️⃣ SQL Chat
> Ask your database questions in plain English!

**What it does:**
- Ask questions in English
- AI converts to SQL automatically
- Shows results as table + plain answer

**Live Demo:** [Coming Soon]
**Tech Stack:** LangChain · SQLite · Few-Shot Learning · Groq · Streamlit

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| **Language** | Python 3.12 |
| **AI Framework** | LangChain, LangGraph |
| **LLM** | Groq (Llama 3) |
| **Vector DB** | FAISS |
| **Frontend** | Streamlit |
| **Database** | SQLite |
| **Search** | DuckDuckGo, Wikipedia |

---

## 📦 Installation
```bash
# Clone repository
git clone https://github.com/Sanchit9A/ai-portfolio.git
cd ai-portfolio

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your API key
# Create .env file and add:
# GROQ_API_KEY=your_key_here

# Run any project
streamlit run rag-news-article/app.py
streamlit run toola-agent/app.py
streamlit run sql-chat/app.py
```

---

## 🔑 API Keys Required

| API | Cost | Get it here |
|---|---|---|
| Groq API | FREE | [console.groq.com](https://console.groq.com) |

---

## 📫 Connect with me
- GitHub: [@Sanchit9A](https://github.com/Sanchit9A)

---

<center>Built with ❤️ using Python and LangChain</center>
```

---

## Save (Ctrl+S)

---

## Your final structure now:
```
ai-portfolio/
├── .gitignore          ✅
├── README.md           ✅ beautiful!
├── requirements.txt    ✅
├── rag-news-article/
│   └── app.py          ✅
├── toola-agent/
│   └── app.py          ✅
└── sql-chat/
    └── app.py          ✅