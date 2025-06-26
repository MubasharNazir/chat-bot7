from pinecone import Pinecone, ServerlessSpec
import os

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
INDEX_NAME = "rag-index"

pc = Pinecone(api_key=PINECONE_API_KEY)

# Create the index if it doesn't exist
if not pc.has_index(INDEX_NAME):
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,  # 384 for MiniLM
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(INDEX_NAME)

def upsert_embedding(entry_id: str, embedding: list):
    index.upsert(vectors=[{"id": entry_id, "values": embedding}])

def delete_embedding(entry_id: str):
    index.delete(ids=[entry_id])

def query_similar_entries(query_embedding, top_k=3, min_score=0.75):
    # results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True).to_dict()
    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True).to_dict()  # type: ignore
    # Each match: {'id': ..., 'score': ..., 'metadata': {...}}
    return [
        {
            "id": match["id"],
            "score": match["score"],
            "description": match.get("metadata", {}).get("description", "")
        }
        for match in results["matches"] if match["score"] >= min_score
    ] 