import os 
from sentence_transformers import SentenceTransformer
import hashlib
from pathlib import Path
import chromadb
import json

BASE_DIR = Path(__file__).resolve().parent

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

knowledgebase = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "knowledge_base.json"
)

vector_db = chromadb.PersistentClient(
    path=str(BASE_DIR / "erp_vector_db")
)

collection = vector_db.get_or_create_collection(
    name="erp_knowledge_base_minilm")

def chunk():
    with open(knowledgebase,"r",encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        if "knowledge_base" in data:
            data = data["knowledge_base"]
        else:
            data = [data]
    
    chunks = []

    for record in data:
        chunk  = (
            f"Ticket:{record['ticket']}\n"
            f"Module:{record['Module']}\n"
            f"Category:{record['Category']}\n"
            f"Cause:{record['Root_Cause']}\n"
            f"Steps:\n{chr(10).join(record['Steps'])}"
        )

        chunks.append(chunk)

    return chunks

def store_embeddings(chunks):
        if not chunks:
            return 

        embeddings = model.encode(
        chunks,
        batch_size=16,
        show_progress_bar=True,
        convert_to_numpy=True
        ).tolist()

                
        ids = [
        hashlib.sha256(
            chunk.encode("utf-8")
        ).hexdigest()
        for chunk in chunks
        ]

        collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=chunks
        )

if __name__ == "__main__":

    chunks = chunk()
    store_embeddings(chunks)
