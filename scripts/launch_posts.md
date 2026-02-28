# Launch Posts — Draft Copy

## Show HN

**Title:** Show HN: StewardMe — self-hosted AI steward that scans HN/arXiv/GitHub and tells you what to do next

**Body:**

I built an open-source, self-hosted AI advisor that combines journaling with live intelligence scraping to give you personalized, explainable guidance.

How it works: you write journal entries and set goals. StewardMe scrapes 10 sources (HN, GitHub trending, arXiv, Reddit, Product Hunt, RSS feeds, etc.) in the background. A RAG pipeline blends your personal context with external intel and feeds it to an LLM (Claude, OpenAI, or Gemini — your choice). Every recommendation comes with a reasoning trace, and a feedback loop adjusts scoring over time.

It runs as a CLI, a web app (FastAPI + Next.js), or an MCP server for Claude Code. All data stays local — SQLite, markdown files, ChromaDB embeddings. Docker one-liner to get started.

Stack: Python 3.11, ChromaDB, SQLite, FastAPI, Next.js, APScheduler.

Looking for contributors — scrapers, LLM providers, frontend polish, and tests are all good entry points. Issues are labeled.

https://github.com/contractorr/stewardme

---

## r/selfhosted

**Title:** StewardMe — self-hosted AI advisor that scans HN, arXiv, GitHub, Reddit and gives you personalized recommendations

**Body:**

Just open-sourced my personal AI advisor project. It's fully self-hosted — all data stays on your machine (SQLite + markdown files + ChromaDB).

**What it does:**
- Scrapes 10 intelligence sources (HN, GitHub trending, arXiv, Reddit, Product Hunt, RSS, etc.) on a schedule
- You journal and set goals via CLI or web UI
- RAG pipeline combines your context + scraped intel → feeds to Claude/OpenAI/Gemini
- Proactive recommendations with reasoning traces + feedback loop
- Goal tracking, trend detection, deep research

**Run it:**
```
git clone https://github.com/contractorr/stewardme.git
cd stewardme
docker compose up --build
```

Or `pip install -e ".[all-providers]"` and use the `coach` CLI.

AGPL-3.0. Contributions welcome — check the issues for `good first issue` labels.

https://github.com/contractorr/stewardme

---

## r/Python

**Title:** StewardMe — RAG-based personal AI advisor built with Python (ChromaDB + FastAPI + Click)

**Body:**

Built an open-source AI advisor that uses RAG to give personalized guidance from your journal entries + live intelligence scraping.

**Interesting technical bits:**
- 10 async scrapers inheriting a `BaseScraper` class, SQLite storage with URL + content-hash dedup
- ChromaDB for journal embeddings, KMeans clustering for trend detection
- Unified `LLMProvider` interface — auto-detects Claude/OpenAI/Gemini from env vars
- RAG retriever with dynamic journal/intel weighting based on engagement data
- FastAPI backend with Fernet-encrypted API key storage
- Click CLI with Pydantic config validation + structlog
- MCP server exposing 22 tools for Claude Code integration
- Tenacity retries + token bucket rate limiting

It's my daily driver for staying on top of HN, arXiv, GitHub trending, Reddit, and turning that into actionable next steps.

Looking for contributors, especially around: new scrapers, Ollama/local model support, test coverage, frontend polish.

https://github.com/contractorr/stewardme

---

## r/LocalLLaMA (post after Ollama provider ships, issue #26)

**Title:** StewardMe — self-hosted AI advisor now with Ollama support

**Body:**

StewardMe is an open-source AI steward that scrapes intelligence sources and combines them with your journal/goals via RAG to give personalized guidance.

Just shipped Ollama support — now runs 100% local with no API keys needed. Pick your model in config.yaml and go.

Fully self-hosted: SQLite, markdown files, ChromaDB. CLI + web UI + MCP server.

https://github.com/contractorr/stewardme
