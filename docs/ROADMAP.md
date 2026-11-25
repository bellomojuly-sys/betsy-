# Roadmap

Copy of the Betsy plan in Notion (agreed 24 November 2026), which stays the source of truth.
Everything is built before the final portfolio of 15 January 2027, at most 12 hours a week.
No work from 23 December 2026 to 4 January 2027.

## G00 Foundations · 24–28 Nov 2026 · *in progress*

Goal: choose a stack and be able to explain why.

- [x] Requirements (24 Nov)
- [x] Weekly hours: at most 12 (24 Nov)
- [x] Plan and study method (24 Nov)
- [ ] Decision Log: stack (single agent in Python, LangGraph or other)
- [ ] Decision Log: positioning of Betsy (single site, neutral, explainable, configurable approval)
- [ ] Decision Log: why independent restaurants in Eindhoven
- [x] Niche card with real data + persona (25 Nov)
- [x] Repo with docs/ROADMAP.md (25 Nov)
- [x] Two mock restaurant profiles (25 Nov)

## G01 One agent · 1–5 Dec 2026

Goal: agent loop, tool calling, structured output, human approval.

- [ ] Study: LLM call vs workflow vs agent; tool calling with JSON schema; structured output; the loop and when it stops; human approval
- [ ] Explain back + check questions
- [ ] Build: stock message parser
- [ ] Build: order proposal per supplier with a reason; approve / edit / reject
- [ ] Tests green, evidence saved, merged to main
- [ ] Gate + Decision Log: why does Betsy start as one agent?

## G02 MCP + RAG · 8–12 Dec 2026

Goal: MCP and permissions; embeddings, chunking, retrieval with citations.

- [ ] Study: MCP host, client and server; tools vs resources; least privilege and tool poisoning; embeddings; chunking; retrieval with citations
- [ ] Explain back + check questions
- [ ] Build: small MCP server (profile, stock)
- [ ] Build: supplier knowledge base (~10 mock documents)
- [ ] Tests green, evidence saved, merged to main
- [ ] Gate + Decision Log: MCP or plain tools? How to chunk supplier documents?

## G03 Measure · 14–18 Dec 2026 · V1 (check-in 3)

Goal: evaluation, tracing, model selection.

- [ ] Study: evaluation scenarios; metrics (success, tool accuracy, cost, latency); tracing; comparing models fairly
- [ ] Explain back + check questions
- [ ] Build: 12 scenarios + 3 injection cases
- [ ] Build: tracing and monitoring dashboard v1
- [ ] Build: model comparison
- [ ] Check-in snapshot ready on Thursday
- [ ] Gate + Decision Log: which model does each agent use?

## Theory · 21–22 Dec 2026

Goal: reach January with the theory already done (notes only).

- [ ] Why split into agents; supervisor pattern; handoffs and failure modes
- [ ] n8n: triggers, nodes, webhooks

## G04 Team · 5–8 Jan 2027

Goal: orchestration, memory, guardrails.

- [ ] Study: supervisor pattern deep-dive; short and long-term memory; prompt injection and guardrails
- [ ] Build: orchestrator + Stock, Purchasing, Receiving & invoice, Supplier agents
- [ ] Build: memory table + guardrail
- [ ] Team vs single agent on the evaluation set
- [ ] Gate + Decision Log: is the team better than one agent?

## G05 n8n · 11–12 Jan 2027

Goal: workflow tool vs agent. First to be cut if behind schedule (becomes a documented experiment).

- [ ] Study: n8n deep-dive
- [ ] Build: one n8n workflow (incoming email → Betsy run)
- [ ] Decision Log: n8n or code for the entry layer?

## V2 Final portfolio · 13–15 Jan 2027

Goal: assembly only, no new work.

- [ ] Collection guide
- [ ] Evidence tags
- [ ] Reflection
