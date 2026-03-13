import streamlit as st
import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ── Load environment variables ──────────────────────────────────────────────
load_dotenv()

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SQL Chat — Ask Your Database",
    page_icon="🗄️",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;600&display=swap');
  html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #0f1117;
    color: #e2e8f0;
  }
  .main-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.5rem;
    font-weight: 500;
    color: #22d3ee;
    margin-bottom: 0.2rem;
  }
  .sub-title { font-size: 1rem; color: #64748b; margin-bottom: 2rem; }
  .answer-box {
    background: #1e293b;
    border-left: 4px solid #22d3ee;
    border-radius: 8px;
    padding: 1.5rem;
    margin-top: 1rem;
    font-size: 1rem;
    line-height: 1.8;
    color: #e2e8f0;
  }
  .sql-box {
    background: #0d1117;
    border: 1px solid #22d3ee;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin-top: 0.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.9rem;
    color: #22d3ee;
  }
  .step-badge {
    background: #22d3ee;
    color: #000;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    margin-right: 8px;
  }
  .stTextInput > div > div > input {
    background: #1e293b !important;
    color: #e2e8f0 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
  }
  .stButton > button {
    background: linear-gradient(90deg, #0891b2, #22d3ee) !important;
    color: #000 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 2rem !important;
    width: 100%;
  }
  section[data-testid="stSidebar"] {
    background-color: #0d1117 !important;
    border-right: 1px solid #1e293b;
  }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🗄️ SQL Chat</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Ask questions in plain English → AI writes SQL → You get answers!</div>', unsafe_allow_html=True)
st.divider()

# ── Create database ───────────────────────────────────────────────────────────
def init_database():
    if not os.path.exists("school.db"):
        conn = sqlite3.connect("school.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            grade TEXT,
            marks INTEGER,
            subject TEXT,
            city TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            subject TEXT,
            experience INTEGER,
            salary INTEGER,
            city TEXT
        )
        """)

        students = [
            (1, "Rahul Sharma", 15, "A", 92, "Math", "Mumbai"),
            (2, "Priya Patel", 16, "B", 78, "Science", "Delhi"),
            (3, "Amit Kumar", 15, "A", 95, "Math", "Bangalore"),
            (4, "Sneha Singh", 17, "C", 65, "English", "Mumbai"),
            (5, "Raj Verma", 16, "B", 82, "Science", "Pune"),
            (6, "Anita Desai", 15, "A", 88, "Math", "Delhi"),
            (7, "Vikram Nair", 17, "B", 75, "English", "Chennai"),
            (8, "Pooja Mehta", 16, "A", 91, "Science", "Mumbai"),
            (9, "Suresh Rao", 15, "C", 60, "Math", "Hyderabad"),
            (10, "Deepa Joshi", 17, "A", 94, "Science", "Pune"),
            (11, "Arjun Gupta", 16, "B", 80, "Math", "Delhi"),
            (12, "Kavya Reddy", 15, "A", 89, "English", "Bangalore"),
            (13, "Rohan Das", 17, "C", 58, "Science", "Mumbai"),
            (14, "Meera Pillai", 16, "B", 77, "Math", "Chennai"),
            (15, "Karan Malhotra", 15, "A", 96, "Science", "Delhi"),
        ]

        teachers = [
            (1, "Mr. Sharma", "Math", 10, 55000, "Mumbai"),
            (2, "Mrs. Patel", "Science", 8, 48000, "Delhi"),
            (3, "Mr. Kumar", "English", 15, 62000, "Bangalore"),
            (4, "Mrs. Singh", "Math", 5, 42000, "Pune"),
            (5, "Mr. Verma", "Science", 12, 58000, "Mumbai"),
            (6, "Mrs. Desai", "English", 7, 45000, "Chennai"),
            (7, "Mr. Nair", "Math", 20, 75000, "Delhi"),
            (8, "Mrs. Mehta", "Science", 3, 38000, "Hyderabad"),
        ]

        cursor.executemany(
            "INSERT OR IGNORE INTO students VALUES (?,?,?,?,?,?,?)",
            students
        )
        cursor.executemany(
            "INSERT OR IGNORE INTO teachers VALUES (?,?,?,?,?,?)",
            teachers
        )

        conn.commit()
        conn.close()

# ── Initialize database ───────────────────────────────────────────────────────
init_database()

# ── Get database schema ───────────────────────────────────────────────────────
def get_schema():
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    schema = ""
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        schema += f"\nTable: {table_name}\n"
        schema += "Columns: " + ", ".join([f"{col[1]} ({col[2]})" for col in columns]) + "\n"
    conn.close()
    return schema

# ── Run SQL query ─────────────────────────────────────────────────────────────
def run_sql(query: str):
    try:
        conn = sqlite3.connect("school.db")
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df, None
    except Exception as e:
        return None, str(e)

# ── Few Shot Examples ─────────────────────────────────────────────────────────
few_shot_examples = [
    {
        "question": "How many students are there?",
        "sql": "SELECT COUNT(*) as total_students FROM students;"
    },
    {
        "question": "Show all students with grade A",
        "sql": "SELECT * FROM students WHERE grade = 'A';"
    },
    {
        "question": "What is the average marks of students?",
        "sql": "SELECT AVG(marks) as average_marks FROM students;"
    },
    {
        "question": "Show top 5 students by marks",
        "sql": "SELECT name, marks FROM students ORDER BY marks DESC LIMIT 5;"
    },
    {
        "question": "How many students are from Mumbai?",
        "sql": "SELECT COUNT(*) as mumbai_students FROM students WHERE city = 'Mumbai';"
    },
    {
        "question": "What is the highest salary among teachers?",
        "sql": "SELECT MAX(salary) as highest_salary FROM teachers;"
    },
    {
        "question": "Show all Math teachers",
        "sql": "SELECT * FROM teachers WHERE subject = 'Math';"
    },
    {
        "question": "Which students scored more than 90 marks?",
        "sql": "SELECT name, marks, subject FROM students WHERE marks > 90;"
    },
]

# ── Build Few Shot Prompt ─────────────────────────────────────────────────────
example_prompt = PromptTemplate(
    input_variables=["question", "sql"],
    template="Question: {question}\nSQL: {sql}"
)

few_shot_prompt = FewShotPromptTemplate(
    examples=few_shot_examples,
    example_prompt=example_prompt,
    prefix="""You are an expert SQL developer.
Given the database schema below, write a SQL query to answer the question.
Return ONLY the SQL query, nothing else. No explanation, no markdown, no backticks.

Database Schema:
{schema}

Here are some examples:""",
    suffix="Question: {question}\nSQL:",
    input_variables=["schema", "question"]
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🗄️ Database Schema")
    st.markdown("<br>", unsafe_allow_html=True)
    schema = get_schema()
    st.code(schema, language="sql")
    st.markdown("---")
    st.markdown("### 💡 Try These Questions")
    st.markdown("- How many students are there?")
    st.markdown("- Show all grade A students")
    st.markdown("- Who has the highest marks?")
    st.markdown("- Average marks of all students?")
    st.markdown("- How many teachers teach Math?")
    st.markdown("- Students from Mumbai?")
    st.markdown("- Top 5 students by marks?")
    st.markdown("- Highest paid teacher?")

# ── Main Question Area ────────────────────────────────────────────────────────
st.markdown("### <span class='step-badge'>STEP 1</span> Ask a Question", unsafe_allow_html=True)

question = st.text_input(
    label="question",
    placeholder="e.g. How many students scored above 80?",
    label_visibility="collapsed",
)

ask_btn = st.button("🔍 Get Answer")

if ask_btn:
    if not question.strip():
        st.warning("⚠️ Please type a question first.")
    else:
        with st.spinner("🤖 Converting to SQL and fetching data..."):
            try:
                # ── Build LLM ──
                llm = ChatGroq(
                    groq_api_key=os.getenv("GROQ_API_KEY"),
                    model_name="llama-3.1-8b-instant",
                    temperature=0,
                )

                # ── Generate SQL using few shot prompt ──
                schema = get_schema()
                prompt_text = few_shot_prompt.format(
                    schema=schema,
                    question=question
                )

                chain = llm | StrOutputParser()
                sql_query = chain.invoke(prompt_text)

                # ── Clean SQL query ──
                sql_query = sql_query.strip()
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

                # ── Show generated SQL ──
                st.markdown("### <span class='step-badge'>STEP 2</span> Generated SQL", unsafe_allow_html=True)
                st.markdown(f'<div class="sql-box">{sql_query}</div>', unsafe_allow_html=True)

                # ── Run SQL ──
                df, error = run_sql(sql_query)

                if error:
                    st.error(f"❌ SQL Error: {error}")
                else:
                    # ── Show results table ──
                    st.markdown("### <span class='step-badge'>STEP 3</span> Results", unsafe_allow_html=True)
                    st.dataframe(df, use_container_width=True)

                    # ── Natural language answer ──
                    st.markdown("### <span class='step-badge'>STEP 4</span> Answer in Plain English", unsafe_allow_html=True)
                    answer_prompt = f"""
Question asked: {question}
SQL result data: {df.to_string()}
Give a clear simple answer in 1-2 sentences based on the data.
"""
                    answer = chain.invoke(answer_prompt)
                    st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ── Database Preview ──────────────────────────────────────────────────────────
st.divider()
st.markdown("### 📊 Database Preview")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**👨‍🎓 Students Table**")
    conn = sqlite3.connect("school.db")
    students_df = pd.read_sql_query("SELECT * FROM students", conn)
    conn.close()
    st.dataframe(students_df, use_container_width=True)

with col2:
    st.markdown("**👨‍🏫 Teachers Table**")
    conn = sqlite3.connect("school.db")
    teachers_df = pd.read_sql_query("SELECT * FROM teachers", conn)
    conn.close()
    st.dataframe(teachers_df, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    "<center style='color:#444;font-size:0.8rem'>Built with LangChain · SQLite · Groq · Few-Shot Learning · Streamlit</center>",
    unsafe_allow_html=True,
)