from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from tools.create_cornell_resume import create_cornell_resume
import logging
import traceback
import asyncio
from fastapi import HTTPException

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

server = FastMCP("cornell-resume", timeout=600)

class ResumeRequest(BaseModel):
    url: str | None = None
    text: str | None = None

@server.tool("create_cornell_resume", description="From the content of this window chat, generate a Cornell Resume and save it to Notion")
async def handle_create_cornell_resume(params: dict):
    try:
        logger.info(f"Received request: {params}")
        resume_request = ResumeRequest(**params)
        
        result = await asyncio.wait_for(
            create_cornell_resume(resume_request),
            timeout=550  
        )
        
        logger.info(f"Request completed successfully: {result}")
        return result
    except asyncio.TimeoutError:
        logger.error("Operation timed out after 550 seconds")
        raise HTTPException(status_code=504, detail="Operation timed out")
    except Exception as e:
        logger.error(f"Error in create_cornell_resume: {str(e)}")
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    logger.info("Starting server...")
    server.run()
