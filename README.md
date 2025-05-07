# MCP: Cornell Resume: UNDER CONSTRUCTION

A service that generates Cornell-style to your Notion summaries from text or URLs, using AI for content analysis and organization.

## Features

- Automatically generates Cornell-style summaries
- Creates content embeddings for semantic analysis
- Automatically tags content
- Saves results to Notion
- Uses MCP for efficient prompt and resource management
- Structured JSON output following Notion API specifications

## Requirements

- Python 3.13+
- OpenAI account
- Pinecone account
- Notion account
- MCP CLI

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Unix/MacOS
   ```
3. Install dependencies:
   ```bash
   uv pip sync requirements.txt
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
NOTION_API_KEY=your_notion_api_key
NOTION_DATABASE_ID=your_database_id
```

## Usage

The service exposes an endpoint that accepts text or URL to generate the summary:

```python
# Usage example
params = {
    "text": "Your text here"  # or "url": "https://example.com"
}
result = await create_cornell_resume(params)
```

### MCP Integration

The service uses MCP for efficient prompt and resource management:

- **Resources**: Templates for Notion block structure are managed through MCP
- **Prompts**: Cornell summary generation prompts are managed through MCP
- **Tools**: The main functionality is exposed as an MCP tool

### Notion Integration

The service generates summaries in the exact format required by the Notion API:

- Uses proper block structure with `rich_text` arrays
- Supports multiple block types (callout, column_list, headings, etc.)
- Maintains proper nesting of properties
- Follows Notion's API specifications

## Contributing

[Section pending development]

## License

MIT License - see LICENSE file for details
