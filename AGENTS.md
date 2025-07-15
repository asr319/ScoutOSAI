⚠️ BekonOS (c) 2025 asr319. All rights reserved. Proprietary License – see LICENSE for terms.
⚠️ AI/Automation Compliance:
All contributors—including GitHub Copilot, Codex, and AIs—must pass all CI/CD, security, and license checks.
See AGENTS.md and workflows for requirements.

# AGENTS.md – BekonOS

Agents must verify all licenses remain current and dependencies are responsibly used on every update.

Last updated: 2025-07-15
Scan status: All checks passed on 2025-07-15

## Purpose

This document provides guidance for any agent (bot, AI model, plugin, or service) that assists with the BekonOS project.
Agents can be LLMs, traditional bots, integrations, or external tools.
All agents must follow these principles to maintain reliability, extensibility, and user trust.

## License and Dependency Compliance

All third-party packages must use compatible licenses. Agents verify licensing and dependency status on every update and replace or remove any with problematic terms. Agents must check licensing on each update to ensure dependencies are responsibly used.

## License Compliance Policy

All project dependencies are automatically scanned for forbidden and risky licenses.  
Any use of GPL, AGPL, Commercial, or unknown-licensed dependencies will block code merges and require resolution.  
Last scan: 2025-07-15 — Status: PASS
See LICENSES-python.md and LICENSES-node.md for a current, full list.

## Other Guides

Additional `AGENTS.md` files are available in `bekonos-backend/` and `bekonos-frontend/`.
Refer to those documents for backend- and frontend-specific instructions.

All agents must install project dependencies before starting any tasks. Use `pip install -r bekonos-backend/requirements.txt -r bekonos-backend/requirements-dev.txt` and run `pnpm install` inside `bekonos-frontend`.

## All logs should be stored in the `logs/` directory (e.g., `logs/agents.log`). Do not record logs inside source files.

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

### Current Agent Contracts

Input and output schemas for built-in agents reside in
`bekonos-backend/app/models` and are enforced via Pydantic models. Agents must
conform to these schemas or extend them with backward-compatible fields.
The script `scripts/validate_agents.py` verifies all AGENTS files contain the
required policy lines and metadata.

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
- Verify all third-party dependencies have current, compatible licenses. Check
  license status and update or replace problematic packages whenever the
  repository changes.

---

## 6. Example: Agent Registration

Add new agent to registry/config (example pseudocode):

```json
{
  "name": "ai-tagger",
  "route": "/ai/tags",
  "input_schema": { "content": "string" },
  "output_schema": { "tags": ["string"] },
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
- Periodically review this file to ensure automation instructions remain current. Record updates in `logs/agents.log`.
- Link to detailed agent/plugin docs as needed.
- Encourage all contributors (human or bot) to suggest improvements.
- BekonOS’s success relies on reliable, transparent, and extensible agent collaboration.
- Agents: Always be helpful, clear, and secure.

## Pull Request Checklist

- Fetch the latest changes from the repository before creating a branch or pull request.
- Check for merge conflicts and resolve them locally.
- Ensure all conflicts are addressed before submitting the pull request.
- Install backend dependencies with `pip install -r bekonos-backend/requirements.txt -r bekonos-backend/requirements-dev.txt`.
- Install frontend dependencies with `pnpm install` in `bekonos-frontend`.
- Run the redundancy checker `python scripts/check_duplicates.py` from the repository root and remove or merge any duplicates.
- Format all project files with `prettier --write .` to keep the codebase tidy. Generate `.min.js` and `.min.css` files using your preferred minifier.

### Local Test Mode

Set `AGENT_BACKEND=local` (or `MOCK_AI=true`) to disable external API calls.
Agents will return stubbed data so you can develop and test BekonOS
completely offline.

---

**Would you like to add a section for agent “personalities” (e.g., formal, friendly, concise), or want a template for agent-specific markdown files?
If you want a copy-paste agent registry file, plugin manifest, or more “how-to” for chaining, just ask!**

## 10. CI/CD, Security, and Agent Policy

BekonOS requires that every Pull Request passes a full suite of automated
checks defined in `.github/workflows/full-checks.yml`. These checks include:

- Secret scanning (Gitleaks and custom Python script)
- Dependency vulnerability audits for JavaScript (`pnpm audit`) and Python
  (`pip-audit`)
- Linting and formatting (`pnpm lint`, `flake8`, `black`, `prettier`)
- Unit and integration tests for both frontend and backend
- Duplicate and error scanning via a Python script
- AGENTS file validation to ensure policies are up to date
- Spelling checks with `pyspelling`
- License compliance for all dependencies. Agents must verify that every
  update keeps package licenses current and remove or replace any that become
  incompatible.
- Static analysis with `bandit` and JS/TS tooling
- Dead code and unused dependency detection
- Coverage enforcement (fail if below 85%)
- Frontend accessibility tests
- Container image vulnerability scans
- Changelog and semantic version bump enforcement
- Repository history secret scan

Branch protection rules require all of these jobs to pass before merging. All
commit and PR messages must contain the line:

`All CI/CD, security, and agent checks passed.`

If any check fails, the Codex Agent automatically attempts to resolve the issue
and re-run the workflow. The agent only submits or approves the PR when all
checks succeed. AGENTS files themselves are kept in sync and validated during
CI.

## Policy Enforcement

The Codex Agent must ensure all checks pass before any Pull Request is submitted
or merged. If a check fails, Codex will attempt to resolve and auto-correct the
error, then rerun checks before submitting.

## BekonOS Brand Kit

Use assets/bekonos-logo.svg in UI and docs. Primary color #20467A, accent #5376A6, yellow #FFD94A. Headlines use Montserrat; body uses Inter. Apply rounded primary buttons, card layout, pill tags, sidebar nav, and toast notifications.
