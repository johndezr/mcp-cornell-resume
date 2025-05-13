from pinecone import Pinecone
from config import PINECONE_API_KEY
import logging

logger = logging.getLogger(__name__)

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("cornell-resumes")

async def query_notes(embedding):
    try:
        result = index.query(vector=embedding, top_k=3, score_threshold=0.6, include_metadata=True)
        logger.info(f"PINECONE QUERY RELATED NOTES: {result}")
        return result.matches[0].metadata["summary"] if result.matches else ""
    except Exception as e:
        logger.error(f"Error in query_notes: {str(e)}")
        raise e

async def upsert_note(embedding, metadata):
    try:
        index.upsert(vectors=[{"id": metadata["id"], "values": embedding, "metadata": metadata}])
        logger.info(f"PINECONE UPSERT NOTE: {metadata}")
        return metadata["id"]
    except Exception as e:
        logger.error(f"Error in upsert_note: {str(e)}")
        raise e