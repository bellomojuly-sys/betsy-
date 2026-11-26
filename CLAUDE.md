# Working rules for Betsy

1. **Read Notion first.** Before writing any code, read the Betsy plan and the current gate's task
   in Notion (Home / University / Betsy, and the "Betsy · Gxx" tasks in Home / System / Tasks).
   Notion is the source of truth; `docs/ROADMAP.md` is a copy of it.
2. **Only the current gate.** Write code and create folders only for the gate in progress.
   Nothing from future gates: no placeholders, no "ready for later" code.
3. **One agent at a time.** Agents are added one by one, and each agent does only a few things.
   No multi-agent structure before G04.
4. **No stack decisions on my own.** Frameworks and libraries are chosen by the owner in the
   Decision Log (`docs/decisions/`). Until then, the repository stays stack-neutral.
5. **Ask before acting** when the request is ambiguous: ask questions first to check that the
   request is understood.
6. **English** for code, comments and documents in this repository.
7. Mock data is provided by the owner; do not invent it.
8. **End-of-session recap.** Before every session ends, without being asked, tell the owner
   (in Italian) four things: what was done (files, commits, Notion), what is left (open work,
   next step, blockers), what the owner must check (code, tests, decisions, anything not pushed
   or not copied to Notion), and the key concepts the session touched (one line each).
