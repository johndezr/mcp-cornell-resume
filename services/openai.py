from openai import OpenAI
from config import OPENAI_API_KEY
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=OPENAI_API_KEY,
)

def load_template(template_name):
    template_path = Path(__file__).parent.parent / "prompts" / template_name
    with open(template_path, "r") as f:
        return f.read()

def load_resource(resource_name):
    resource_path = Path(__file__).parent.parent / "resources" / resource_name
    with open(resource_path, "r") as f:
        return f.read()

async def generate_cornell_summary(content):
    prompt_template = load_template("cornell_summary_prompt.txt")
    notion_template = load_resource("notion_block_template.json")
    
    prompt = prompt_template.replace("{{notion_block_template}}", notion_template)
    prompt = prompt.replace("{{content}}", content)
    
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
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
