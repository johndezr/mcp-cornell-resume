from pinecone import Pinecone
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME
import logging

logger = logging.getLogger(__name__)

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

async def query_notes(embedding):
    try:
        result = index.query(vector=embedding, top_k=3, score_threshold=0.5, include_metadata=True)
        logger.info(f"PINECONE QUERY RELATED NOTES: {result}")
        summaries_text = "\n".join([match.metadata["title"] for match in result.matches])
        return summaries_text
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