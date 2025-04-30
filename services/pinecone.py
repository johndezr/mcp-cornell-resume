from pinecone import Pinecone
from config import PINECONE_API_KEY
import logging

logger = logging.getLogger(__name__)

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("tags-index")

async def query_tags(embedding):
    try:
        result = index.query(vector=embedding, top_k=5, include_metadata=True)
        tags = [match["metadata"]["tag"] for match in result["matches"]]
        logger.info(f"PINECONE QUERY TAGS: {tags}")
        return tags
    except Exception as e:
        logger.error(f"Error en query_tags: {str(e)}")
        raise e
