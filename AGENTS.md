# AGENTS.md – ScoutOSAI

## Purpose

This document provides guidance for any agent (bot, AI model, plugin, or service) that assists with the ScoutOSAI project.
Agents can be LLMs, traditional bots, integrations, or external tools.
All agents must follow these principles to maintain reliability, extensibility, and user trust.

## Other Guides

Additional `AGENTS.md` files are available in `scoutos-backend/` and `scoutos-frontend/`.
Refer to those documents for backend- and frontend-specific instructions.

---

## 1. What Is an Agent?

An **agent** is an autonomous or semi-autonomous process that:
- Receives structured input (e.g., user queries, memory data, tags)
- Processes it using logic, LLMs, external APIs, or plugins
- Returns structured output (e.g., chat reply, suggested tags, merge/summarize results)
- May initiate further actions (e.g., save, search, escalate, notify)

Agents include:
- LLM endpoints (OpenAI, local Llama, Claude, etc.)
- Search bots (web, docs, plugin directories)
- Memory and merge suggestion engines
- Taggers, summarizers, and QA/retrieval services
- External service integrations (Notion, Slack, GitHub, etc.)

---

## 2. How Should Agents Interact?

### **API Contracts**
- Expose all agent actions as REST endpoints or plugin hooks (`/ai/chat`, `/ai/tags`, `/ai/merge`, `/search`, etc.)
- Accept JSON input, return JSON output.
- Support `input`, `options`, and `meta` fields in payloads for extensibility.

### **Frontend/UI**
- Agents may be invoked automatically (on memory creation, merge detection, etc.) or by user request.
- Always return clear, actionable responses (with reason/explanation when possible).
- Provide suggestions, never force changes without user approval (unless specifically configured).

### **Agent Chaining**
- Agents can call other agents in sequence (e.g., tag → summarize → suggest merge).
- Maintain modularity—agents should be swappable and composable.

---

## 3. Agent Onboarding/Extension

- New agents should register themselves (or be registered) in the agent registry/config.
- Document their input/output schemas and options in `agents.md` or a linked doc.
- Clearly indicate any required credentials (API keys, env vars) and scope of action.
- Support dry-run/test mode for debugging or review.

---

## 4. How to Assist Developers, Users, and Other Bots

- Respond to user and developer requests with concise, context-aware advice or actions.
- Suggest next steps, code templates, or API docs as appropriate.
- When uncertain, ask for clarification rather than guessing.
- If agent chaining, always document and log the chain for traceability.
- Offer to summarize, analyze, or recommend plugins or next actions.

---

## 5. Rules, Best Practices, and Safeguards

- Never expose secrets (API keys, tokens) in any frontend/UI or logs.
- Rate-limit and validate all external calls (especially paid APIs).
- Use the principle of least privilege—request only the data needed for the task.
- If a request is ambiguous, prompt the user or developer for details.
- Always log errors and warnings in a secure, privacy-compliant way.
- Support hot-swapping of agent backends via config or env (e.g., OpenAI → Llama).

---

## 6. Example: Agent Registration

Add new agent to registry/config (example pseudocode):

```json
{
  "name": "ai-tagger",
  "route": "/ai/tags",
  "input_schema": {"content": "string"},
  "output_schema": {"tags": ["string"]},
  "dependencies": ["OPENAI_API_KEY"],
  "description": "Suggests tags for memory objects using LLM."
}
```

### Registering New Agent Types

Agent metadata is stored in the `agent_configs` table. Create or update a record
by posting the `name`, `enabled` flag and optional `settings` JSON to
`/agent/config`. Toggle an agent on or off with `/agent/enable` and retrieve all
entries using `GET /agent/config`.

## 7. Checklist for New Agent

- Exposes clear endpoint or hook
- Documents input/output
- Registered in agent config
- Follows security and logging rules
- Includes test/dry-run mode if possible

## 8. Escalation and Handoff

If an agent can’t complete a task:

- Clearly indicate failure and suggest next steps.
- Escalate to a human or another agent as defined in project rules.
- Log all handoff attempts for future review.

## 9. Updating This Document

- Keep agents.md up-to-date as new agents, APIs, or workflows are added.
- Link to detailed agent/plugin docs as needed.
- Encourage all contributors (human or bot) to suggest improvements.
- ScoutOSAI’s success relies on reliable, transparent, and extensible agent collaboration.
- Agents: Always be helpful, clear, and secure.

## Pull Request Checklist

- Fetch the latest changes from the repository before creating a branch or pull request.
- Check for merge conflicts and resolve them locally.
- Ensure all conflicts are addressed before submitting the pull request.

---

**Would you like to add a section for agent “personalities” (e.g., formal, friendly, concise), or want a template for agent-specific markdown files?
If you want a copy-paste agent registry file, plugin manifest, or more “how-to” for chaining, just ask!**

