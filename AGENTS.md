# Agents in ScoutOSAI

## What Is an Agent?

In ScoutOSAI, an **agent** is any autonomous or semi-autonomous service or process that can:
- Search, recall, or summarize knowledge
- Execute tasks or queries (e.g., LLMs, search APIs, memory processors)
- Integrate with ScoutOSAI via API calls or plugin hooks

Agents are modular—new agents can be added to extend system capability, such as:
- Large Language Models (LLMs) like OpenAI GPT, Mistral, Llama, etc.
- Web search APIs (Google, DuckDuckGo, Bing)
- Custom plugins (Notion, Slack, GitHub, calendar, etc.)
- Local or remote knowledge bases

---

## Core Agent Types

| Type           | Description                                     | Example                      |
|----------------|-------------------------------------------------|------------------------------|
| AI/LLM Agent   | Text generation, summarization, tagging, merge  | OpenAI, local Llama, Mistral |
| Search Agent   | Web or internal search queries                  | Bing API, DuckDuckGo         |
| Memory Agent   | Custom logic for recall, deduplication, merging | ScoutOSAI memory merge agent |
| Integration    | Third-party app/plugin connector                | Notion, Slack, GitHub, etc.  |

---

## How Agents Work

- Agents are exposed as backend API routes (e.g., `/ai/chat`, `/search/web`, `/agent/merge`)
- The frontend may have panels or triggers to interact with specific agents
- Agents can be chained (e.g., use LLM to summarize search results or auto-tag a memory)
- Each agent follows a standard request/response contract (see below)

---

## Agent API Contract (Typical)

```json
POST /agent/[agent_type]
{
  "input": "...",        // prompt, query, or memory block
  "options": { ... }     // agent-specific options
}
→
{
  "output": "...",       // result (e.g., generated text, search results)
  "agent": "OpenAI GPT-4",
  "meta": { ... }
}
```
