from sentence_transformers import SentenceTransformer
import chromadb

class RAGRetriever:
    
    """
    This RAG class will initialize the chromadb client when invoked and store the vector enbedding of faq.txt file using sentence embedding model: 'all-MiniLM-L6-v2
    """
    
    def __init__(self, kb_path="faq.txt"):
        self.kb_path = kb_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection("testing_collection")
        self.docs = []
        self.build_index()

    def build_index(self):
        with open(self.kb_path, 'r') as f:
            content = f.read()
        self.docs = [para.strip() for para in content.split("\n\n") if para.strip()]

        embeddings = self.model.encode(self.docs).tolist()
        for i, (doc, emb) in enumerate(zip(self.docs, embeddings)):
            self.collection.add(
                ids=[str(i)],
                documents=[doc],
                embeddings=[emb]
            )

    def query(self, user_input, top_k=1):
        query_embedding = self.model.encode([user_input])[0].tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents']
        )
        return results['documents'][0]

