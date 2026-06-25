# Manga Recommendation Discord Bot

This project is a Discord AI bot that recommends manga, manhwa, and manhua based on user messages using semantic embeddings and LLM-based intent classification.

The system combines:
- Large language model classification (Groq API)
- Text embedding generation (Jina embeddings API)
- Cosine similarity search over a precomputed manga database
- Discord real-time message processing

---

## Features

- Detects whether a user is requesting manga/manhwa/manhua recommendations
- Uses an LLM to classify user intent into structured JSON
- Generates semantic embeddings for user queries
- Finds similar titles using cosine similarity search
- Returns ranked recommendations with metadata (rating, tags, year, cover)

---

## How it works

1. User sends a message in a monitored Discord channel
2. LLM classifies the message:
   - If not a request → bot replies with a helper message
   - If request → continue pipeline
3. User message is cleaned and embedded using Jina embeddings
4. Cosine similarity is computed against stored manga embeddings
5. Top matching titles are retrieved and sent to Discord

---

## Dataset

The bot uses a precomputed library stored in:

- titles
- ratings
- tags
- year
- covers
- embeddings

All data is loaded from a local JSON file.

---

## Tech Stack

- Python
- PyTorch
- Discord.py
- Groq API (LLM classification)
- Jina Embeddings API
- Cosine similarity search

---

## Limitations

- Requires external API keys (Groq, Jina)
- No persistent caching layer
- Ranking is based purely on embedding similarity
- No user personalization yet
