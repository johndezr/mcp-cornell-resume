from fastapi import HTTPException
from pydantic import BaseModel
from services.openai import generate_cornell_summary, generate_embeddings
from services.pinecone import query_tags
from services.notion import save_to_notion
import json

class ResumeRequest(BaseModel):
    url: str | None = None
    text: str | None = None

async def create_cornell_resume(params: ResumeRequest):
  if not params.text and not params.url:
      raise HTTPException(status_code=400, detail="You should provide a 'text' or 'url'.")

  content = params.text or f"Content of {params.url} (simulated)"

  summary_str = await generate_cornell_summary(content)
  summary_obj = json.loads(summary_str)
#   embedding = await generate_embeddings(summary)
#   tags = await query_tags(embedding)
  notion_id = await save_to_notion(summary_obj, [])

  return {
      "summary": summary_obj,
      "summary_raw": summary_str,
      "tags": [],
      "notion_id": notion_id
  }
