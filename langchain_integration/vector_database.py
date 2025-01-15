import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorDatabase:
    def __init__(self, embedding_model='all-MiniLM-L6-v2'):

        self.model = SentenceTransformer(embedding_model)
        self.index = faiss.IndexFlatL2(384)  
        self.embeddings = []  
        self.texts = []  

    def add_texts(self, texts):
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        self.index.add(np.array(embeddings).astype('float32'))
        self.embeddings.extend(embeddings)
        self.texts.extend(texts)

    def search(self, query, top_k=3):
        query_embedding = self.model.encode([query], convert_to_tensor=False)
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), top_k)
        results = [(self.texts[idx], distances[0][i]) for i, idx in enumerate(indices[0])]
        return results
