import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from google.generativeai import GenerativeModel , configure
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

embedding_model = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
vector_db = Chroma(persist_directory="db", embedding_function=embedding_model)
configure(api_key=GEMINI_API_KEY)
gemini = GenerativeModel('gemini-2.5-flash')

def answer_query(question, user_role):
    """search vector db,filter by user role,and ask gemini to generate answer"""

    relevant_docs = vector_db.similarity_search(question, k=5)


    
    # filter to keep only chunks allowed for this user role
    filtered = [
        doc for doc in relevant_docs
        if user_role in doc.metadata.get("role_access", "").split(",")
    ]

    if not filtered:
        return {
            "answer": " I'm sorry, you don't have access to this information",
            "sources": []
        }

    

    # making context for gemini model
    context = "\n".join(doc.page_content for doc in filtered)
    prompt = f"Answer the user's question based only on this context:\n{context}\n\nQuestion: {question}"
    
    response = gemini.generate_content(prompt)
    return {
        "answer": response.text,
        "sources": list(set(doc.metadata.get("source_doc") for doc in filtered))
    }
