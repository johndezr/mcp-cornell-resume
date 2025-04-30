from openai import OpenAI
import os
from config import OPENAI_API_KEY
import logging

logger = logging.getLogger(__name__)

client = OpenAI(
    # This is the default and can be omitted
    api_key=OPENAI_API_KEY,
)

async def generate_cornell_summary(content):
    prompt = f"""
    With the content provided, create a Cornell note with the following format: notes, cues, summary. Return the response in JSON format.

    Content:
    {content}
    
    Eg:
    {{
        "notes": "...",
        "cues": "...",
        "summary": "..."
    }}
    """
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions="You are an expert in note taking",
            input=prompt,
            text={
                "format": {
                    "type": "json_object"
                }
            }
        )
        text_response = response.output_text
        logger.info(f"text_response: {text_response}")
        return text_response
    except Exception as e:
        logger.error(f"Error en generate_cornell_summary: {str(e)}")
        raise e

async def generate_embeddings(text):
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error en generate_embeddings: {str(e)}")
        raise e
