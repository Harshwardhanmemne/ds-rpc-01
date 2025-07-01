import os
from langchain_community.document_loaders import DirectoryLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

def load_data():
    """
    Loading all our data files from the resources directory and 
    this will grabs both markdown docs and HR data
    """
    all_documents = []
    data_folder = "resources/data"
    
    # getting all the markdown files
    markdown_loader = DirectoryLoader(data_folder, glob="**/*.md")
    markdown_docs = markdown_loader.load()
    all_documents.extend(markdown_docs)
    
    # now load the HR CSV file
    hr_file_path = f"{data_folder}/hr/hr_data.csv"
    hr_loader = CSVLoader(hr_file_path)
    hr_documents = hr_loader.load()
    all_documents.extend(hr_documents)
    
    return all_documents

def split_documents_into_chunks(documents):
    """spliting the big document into teh chunks such that there would be no token limit error 
    i.e. using 500 chars per chunk with some overlap to maintain context"""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, 
        chunk_overlap=50
    )
    document_chunks = text_splitter.split_documents(documents)
    return document_chunks

def setup_vector_database(document_chunks):
    """Creating our vector database where each chunk gets tagged with which roles can access it"""

    # embedding model
    embedding_model = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

    
    #added some metadata to control access by department
    for chunk in document_chunks:
        source_path = chunk.metadata["source"]
        
        #determining access permissions accr to the given PS
        if "finance" in source_path:
            chunk.metadata["role_access"] = "finance,c-level"
        elif "engineering" in source_path:
            chunk.metadata["role_access"] = "engineering,c-level"
        elif "marketing" in source_path:
            chunk.metadata["role_access"] = "marketing,c-level"
        elif "hr" in source_path:
            chunk.metadata["role_access"] = "hr,c-level"
        else:
            # default access for general documents
            chunk.metadata["role_access"] = "employee,engineering,finance,marketing,hr,c-level"
        
        # also to show where does this data come from we save this path info
        chunk.metadata["source_doc"] = os.path.basename(source_path)
    
    #creating the vector database
    vector_db = Chroma.from_documents(
        document_chunks, 
        embedding_model, 
        persist_directory="db"
    )
    vector_db.persist()
    print("vector db created")
    
    return vector_db

if __name__ == "__main__":
    docs = load_data()
    chunks = split_documents_into_chunks(docs)
    setup_vector_database(chunks)
