from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, Docx2txtLoader
from pathlib import Path
import json

def load_file(file_path):
    path = str(file_path)
    
    if path.endswith(".pdf"):
        loader = PyPDFLoader(path)
    elif path.endswith(".txt"):
        loader = TextLoader(path)
    elif path.endswith(".csv"):
        loader = CSVLoader(path)
    elif path.endswith(".docx"):
        loader = Docx2txtLoader(path)
    else:
        return ""
    
    docs = loader.load()
    
    text = ""
    for doc in docs:
        text += doc.page_content + "\n"
    
    return text

raw_dir = Path("src/data/raw")
all_docs = []

for file in raw_dir.glob("*"):
    if file.is_file():
        text = load_file(file)
        if text:
            all_docs.append({"text": text, "source": file.name})
            print(file.name, "Loaded", len(text), "characters")

Path("src/data/cleaned").mkdir(exist_ok=True)
json.dump(all_docs, open("src/data/cleaned/documents.json", "w"), indent=2)
