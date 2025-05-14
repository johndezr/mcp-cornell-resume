from fastapi import HTTPException
from pydantic import BaseModel
from services.openai import generate_cornell_summary, generate_embeddings
from services.notion import save_to_notion
from services.pinecone import upsert_note, query_notes
import json
import uuid

class ResumeRequest(BaseModel):
    url: str | None = None
    text: str | None = None

async def create_cornell_resume(params: ResumeRequest):
  if not params.text and not params.url:
      raise HTTPException(status_code=400, detail="You should provide a 'text'.")

  content = params.text or f"Content of {params.url} (simulated)"

  embedding = await generate_embeddings(content)
  related_notes = await query_notes(embedding)
  summary_str = await generate_cornell_summary(content, related_notes)
  summary_obj = json.loads(summary_str)
  await upsert_note(embedding, { "id": str(uuid.uuid4()), "title": summary_obj["title"], "summary": summary_obj["summary"] })
  notion_id = await save_to_notion(summary_obj, [])

  return {
      "notion_page_id": notion_id
  }
