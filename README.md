# Yggdrasil AI 🌳🦉

A memory-guided autonomous reasoning system inspired by the Minerva's Owl Protocol.

## Features
- Embeds and stores contextual memory in Pinecone
- Retrieves relevant memory for any user question
- Uses OpenAI GPT models to generate responses with memory context
- CLI command: `yggdrasil "What are my active goals?"`

## Setup

```bash
pip install -e .
cp .env.example .env
```

Then run:

```bash
yggdrasil "What does the owl protocol mean?"
```

## Environment Variables

Set these in a `.env` file:

```dotenv
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=pcsk-...
```

## License
MIT
