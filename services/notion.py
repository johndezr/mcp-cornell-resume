import requests
import logging

logger = logging.getLogger(__name__)

from dotenv import load_dotenv
from config import NOTION_DATABASE_ID, NOTION_API_KEY
import json

load_dotenv()

async def save_to_notion(summary, tags):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    data = {
        "parent": { "database_id": NOTION_DATABASE_ID },
        "properties": {
            "Name": { "title": [{ "text": { "content": (summary["title"] if summary["title"] else "No title") } }] },
        },
        "children": summary["blocks"]
    }
    try: 
        response = requests.post(url, headers=headers, json=data)
        logger.info(f"NOTION RESPONSE: {response.json()}")
        return response.json().get("id")
    except Exception as e:
        logger.error(f"Error en save_to_notion: {str(e)}")
        raise e
