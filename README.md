# Simple CrewAI Code Walkthrough

This tiny demo matches the CrewAI code on the workshop PPT:
**Agent → Task → Crew → Process.sequential → kickoff()**

Run `run_windows.bat`.

If `.env` has no Groq key, the script runs a deterministic fallback.
If a Groq key is present, it runs the real CrewAI crew.

For the live walkthrough, explain only:
1. Agent = who
2. Task = what
3. context = handoff of previous work
4. Crew = team
5. Process.sequential = order
6. kickoff() = execute

Default Groq model: `openai/gpt-oss-20b`
