# LinkedIn Article Agent

A CrewAI-based agent chain that generates well-researched LinkedIn articles by:
1. **Researching** the topic using Perplexity API
2. **Planning** the article structure and key points
3. **Writing** a complete, polished article

## Features

- 🔍 **Web Research**: Leverages Perplexity API for real-time information gathering
- 📋 **Intelligent Planning**: Generates structured article outlines in Markdown
- ✍️ **Content Generation**: Writes engaging LinkedIn articles based on research and plans
- 🔧 **Flexible Input**: Accepts article topics and skeleton structures
- 💾 **Output Management**: Saves plans and articles for review and editing

## Setup

### Prerequisites
- Python 3.10+
- Perplexity API key
- OpenAI API key (for LLM capabilities)

### Installation

1. Clone or navigate to the project directory
2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

## Usage

Run the article generation workflow:
```bash
python main.py --topic "Your Article Topic" --skeleton "path/to/skeleton.md"
```

### Example

```bash
python main.py \
  --topic "The Future of AI in Enterprise" \
  --skeleton "article_skeleton.md"
```

This will:
1. Research the topic using Perplexity
2. Generate a plan in `outputs/plan.md`
3. Write the full article in `outputs/article.md`

## Project Structure

```
agents/
├── src/
│   ├── agents/           # Agent definitions
│   ├── tasks/            # Task definitions
│   ├── config.py         # Configuration and setup
│   └── tools/            # Custom tools and utilities
├── main.py               # Entry point
├── pyproject.toml        # Project metadata
├── requirements.txt      # Dependencies
└── outputs/              # Generated articles and plans
```

## Architecture

### Agents
- **Research Agent**: Gathers information from web via Perplexity API
- **Planning Agent**: Structures the research into a coherent outline
- **Writing Agent**: Crafts the final LinkedIn article

### Tasks
- **Research Task**: Find relevant information on the topic
- **Planning Task**: Create a detailed article plan in Markdown
- **Writing Task**: Generate the complete article

## API Documentation

### Perplexity Integration
The project uses Perplexity API for web research. Ensure your API key is set in `.env`.

## Tips for Best Results

- Provide specific, well-defined article topics
- Include a skeleton structure with key sections you want covered
- Review generated plans before article writing
- Edit outputs as needed for brand voice and style

## Troubleshooting

- **API Key Issues**: Verify your keys are correctly set in `.env`
- **Research Timeouts**: Increase timeout settings in `config.py`
- **Token Limits**: Monitor token usage for large articles

## Future Enhancements

- [ ] Support for multiple target platforms (LinkedIn, Medium, Dev.to)
- [ ] Built-in fact-checking and citation generation
- [ ] Interactive refinement loop
- [ ] Custom writing style templates
- [ ] Batch article generation

## License

This project is for personal use.
