# 🛡️ FinSolve RBAC Chatbot

A Retrieval-Augmented Generation (RAG)-based chatbot with **Role-Based Access Control (RBAC)**, built using:

* FastAPI (backend API)
* LangChain + Chroma (vector database)
* HuggingFace embeddings
* Google Gemini model (LLM)
* Streamlit (frontend UI)

---

## 📌 **Features**

* Authenticate users with different roles (e.g., Engineering, HR, Marketing, Finance, C-Level).
* Store document chunks and metadata (which roles can access which data) in a vector DB.
* Users can ask natural language questions, and chatbot filters answers based on role.
* Modular & clean Python code (FastAPI + Streamlit).
* `.env` based API keys for secure config.

---

## 🧩 **Project Structure**

```
ds-rpc-01/
├─ app/
│  ├─ main.py                # FastAPI backend
│  ├─ build_vector_db.py     # Script to build vector db from documents
│  ├─ chatbot_query.py       # Query logic
│  ├─ ...
├─ frontend/
│  ├─ ui.py                  # Streamlit UI
├─ resources/
│  ├─ data/                  # Markdown & CSV files
├─ db/                       # Vector db (auto-generated)
├─ .env                      # API keys etc.
├─ requirements.txt
├─ README.md
```

---

## ⚙️ **Setup Instructions**

```bash
# 1. Clone the repo
git clone https://github.com/Harshwardhanmemne/ds-rpc-01.git
cd ds-rpc-01

# 2. Create virtual env
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key to .env
echo GEMINI_API_KEY='your_key_here' > .env

# 5. Build vector db
python app/build_vector_db.py

# 6. Start backend
uvicorn app.main:app --reload

# 7. Start frontend
streamlit run frontend/ui.py
```

---

## 🔐 **Roles and Permissions**

| Role        | Can Access                                             |
| ----------- | ------------------------------------------------------ |
| HR          | Employee data, payroll, attendance                     |
| Marketing   | Campaign performance, sales metrics, customer feedback |
| Finance     | Financial reports, expenses, reimbursements            |
| Engineering | Technical docs, architecture, dev processes            |
| C-Level     | All data                                               |
| Employee    | General company info, policies, FAQs                   |

---

## 📦 **Tech Stack**

* FastAPI
* LangChain
* Chroma DB
* HuggingFace embeddings
* Google Gemini
* Streamlit

---

## ✅ **Demo**

* Login with username & password
* Ask role-specific questions
* Chatbot answers only if your role has access

---

## 📚 **Credits**
💡 Built as part of the Codebasics Resume Project Challenge
📘 LangChain learning via CampusX YouTube Channel

---

## 📜 **License**

Open-source for educational use.
