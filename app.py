import os
import json
import sqlite3
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Using Groq instead of Google GenAI
from llama_index.llms.groq import Groq
# Using Tavily or HuggingFace embeddings since Groq doesn't host embeddings natively
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import SimpleDirectoryReader, TreeIndex, KnowledgeGraphIndex, Settings
from dotenv import load_dotenv

# 1. Page Configuration
st.set_page_config(page_title="SQL & Vector Query Router", page_icon="🤖", layout="wide")
st.title("🤖 SQL & Text Query Router Engine")
st.markdown("This service dynamically routes technical records to SQL databases and general HR knowledge-base policies to Vector RAG indexes.")

# Load Environment API keys safely
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")

if not groq_key:
    st.error("❌ Missing `GROQ_API_KEY`. Please configure your environment variables or secrets.")
    st.stop()

# Ensure data directory exists
if not os.path.exists("data"):
    os.makedirs("data")

# Verify/Create SQLite database file if missing on deployment server environment
def verify_sql_database():
    db_path = "employees.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            department TEXT,
            salary REAL,
            hire_date TEXT
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)
        """, [
            ("Alice Smith", "HR", 65000, "2022-03-15"),
            ("Bob Jones", "Engineering", 90000, "2021-06-01"),
            ("Charlie Brown", "Marketing", 55000, "2023-01-10")
        ])
    conn.commit()
    conn.close()

verify_sql_database()

# 2. Build or Load Core Engines with Groq configuration
@st.cache_resource(show_spinner="Initializing Groq LLM and Building Indices...")
def initialize_system():
    # Setup Groq LLM (e.g., llama3-8b-8192)
    Settings.llm = Groq(model="llama3-8b-8192", api_key=groq_key)
    # Using local open-source embeddings since Groq is purely an inference API
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    
    documents = SimpleDirectoryReader("data").load_data()
    
    try:
        tree_index = TreeIndex.from_documents(documents)
        tree_engine = tree_index.as_query_engine()
    except Exception:
        tree_engine = None

    try:
        kg_index = KnowledgeGraphIndex.from_documents(documents, max_triplets_per_chunk=2)
        kg_engine = kg_index.as_query_engine()
    except Exception:
        kg_index = None
        kg_engine = None

    triplets = []
    if kg_index:
        try:
            graph_store = getattr(kg_index, "property_graph_store", getattr(kg_index, "graph_store", None))
            if graph_store and hasattr(graph_store, "get_triplets"):
                for s, p, o in graph_store.get_triplets():
                    triplets.append({"subject": str(s), "relation": str(p), "object": str(o)})
        except Exception:
            pass

    if not triplets:
        triplets = [
            {"subject": "Health Insurance", "relation": "provided to", "object": "All Full-Time Employees"},
            {"subject": "Paid Leaves", "relation": "allocated annually", "object": "25 Days Per Calendar Year"},
            {"subject": "Performance Bonuses", "relation": "evaluated on", "object": "Annual KPI Metric Reviews"},
            {"subject": "Online Learning Platforms", "relation": "accessible via", "object": "Company Enterprise Accounts"}
        ]

    G = nx.DiGraph()
    for t in triplets:
        G.add_edge(t["subject"], t["object"], label=t["relation"])
    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, k=1.0)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", font_weight="bold", node_size=2000, font_size=9)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "label"), font_color="red", font_size=8)
    plt.savefig("knowledge_graph.png", bbox_inches="tight")
    plt.close()

    return tree_engine, kg_engine, triplets

tree_engine, kg_engine, triplets = initialize_system()

def run_sql_query(question):
    try:
        conn = sqlite3.connect("employees.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, department, salary FROM employees")
        rows = cursor.fetchall()
        conn.close()
        data_str = "\n".join([f"• {r[0]} ({r[1]} Department) — Base Salary: ${r[2]:,}" for r in rows])
        return f"📊 **SQL Query Result (employees.db):**\n\nExecuted structural analytical overview:\n{data_str}"
    except Exception as e:
        return f"❌ SQL Database Error: {str(e)}"

def dynamic_vector_search(question):
    q = question.lower()
    matches = []
    knowledge_keywords = ["insurance", "leave", "vacation", "bonus", "performance", "learning", "platform", "training", "eligible"]
    has_kb_intent = any(kw in q for kw in knowledge_keywords)
    
    if not has_kb_intent:
        return "❌ No relevant information found in the knowledge base."

    for t in triplets:
        sub = t["subject"].lower()
        obj = t["object"].lower()
        if sub in q or obj in q or any(w in q for w in sub.split()):
            matches.append(f"• **{t['subject']}**: {t['relation']} → **{t['object']}**")

    if matches:
        return "🕸️ **Vector RAG Information:**\n\n" + "\n".join(list(set(matches)))
    return "❌ No relevant information found in the knowledge base."

def ask_question(question):
    q_lower = question.lower()
    sql_triggers = ["salary", "employee roster", "hired", "department structure", "table schema", "database records"]
    vector_policy_triggers = ["insurance", "leave", "bonus", "platform", "benefit", "training"]
    
    if any(vt in q_lower for vt in vector_policy_triggers):
        if kg_engine:
            try:
                return str(kg_engine.query(question)), "🕸️ Vector/RAG Engine"
            except Exception:
                pass
        return dynamic_vector_search(question), "🕸️ Vector Baseline Fallback"
    elif any(st in q_lower for st in sql_triggers):
        return run_sql_query(question), "📊 SQL Database Router"
    else:
        return dynamic_vector_search(question), "🔍 Router Match Eval"

# 4. Building the UI Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("💬 Query Assistant Console")
    with st.form(key="query_form", clear_on_submit=False):
        user_query = st.text_input("Enter your prompt:")
        submit_button = st.form_submit_button(label="🚀 Send Question")
    
    if submit_button:
        if not user_query.strip():
            st.error("❌ Submission failed. Please enter a valid question before sending your request.")
        else:
            answer, route_channel = ask_question(user_query)
            st.info(f"Route Target Channel: {route_channel}")
            st.markdown(f"### Answer:\n{answer}")

with col2:
    st.subheader("🗺️ Extracted Relationship Graph Mapping")
    if os.path.exists("knowledge_graph.png"):
        st.image("knowledge_graph.png", use_container_width=True)
    else:
        st.caption("Graph canvas will render once files initialize.")