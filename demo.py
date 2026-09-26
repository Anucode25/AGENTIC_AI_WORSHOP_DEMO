import os
import time
import random
import re
import contextlib
import io

# ============================================================
# DISABLE CREWAI TELEMETRY / TRACING
# ============================================================

os.environ["CREWAI_TRACING_ENABLED"] = "false"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"

from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Agentic AI Crew",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# SESSION STATE
# ============================================================

if "final_output" not in st.session_state:
    st.session_state.final_output = ""

if "debug_logs" not in st.session_state:
    st.session_state.debug_logs = []

if "last_task" not in st.session_state:
    st.session_state.last_task = ""


# ============================================================
# DEBUG LOGGER
# ============================================================

def debug(message):
    st.session_state.debug_logs.append(message)


# ============================================================
# DEMO FALLBACK
# ============================================================

def demo_mode(task):

    debug("⚠️ Groq unavailable")
    debug("🟡 Switched to DEMO MODE")

    debug("🧠 Researcher → analyzing task")
    debug("✍️ Writer → generating response")
    debug("🔍 Editor → polishing response")

    return f"""
### Demo Result

The AI crew received your task:

> {task}

The agent workflow is:

**Researcher → Writer → Editor**

This is the fallback demonstration mode.
"""


# ============================================================
# RATE LIMIT HANDLER
# ============================================================

def get_wait_time(error, attempt):

    error_text = str(error).lower()

    patterns = [
        r"retry after ([0-9.]+)",
        r"retry-after[=: ]+([0-9.]+)",
        r"try again in ([0-9.]+)"
    ]

    for pattern in patterns:

        match = re.search(pattern, error_text)

        if match:

            try:
                return float(match.group(1))
            except ValueError:
                pass

    return 8 * (2 ** attempt) + random.uniform(0, 2)


# ============================================================
# RUN CREW
# ============================================================

def run_crew(user_task):

    st.session_state.debug_logs = []

    debug("🚀 Crew execution started")
    debug(f"📌 Task: {user_task}")

    # --------------------------------------------------------
    # API KEY
    # --------------------------------------------------------

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:

        debug("❌ GROQ_API_KEY not found")

        return demo_mode(user_task)

    debug("🔑 Groq API key detected")
    debug("🤖 Model: openai/gpt-oss-20b")

    # --------------------------------------------------------
    # LLM
    # --------------------------------------------------------

    try:

        llm = LLM(
            model="groq/openai/gpt-oss-20b",
            api_key=api_key,
            temperature=0.2,
            max_tokens=250
        )

        debug("✅ LLM initialized")

    except Exception as e:

        debug(f"❌ LLM initialization failed: {e}")

        return demo_mode(user_task)

    # ========================================================
    # AGENTS
    # ========================================================

    debug("🧠 Creating Researcher")

    researcher = Agent(
        role="Researcher",
        goal="Identify the key information required to solve the task.",
        backstory="You are a concise research analyst.",
        llm=llm,
        verbose=False,
        max_iter=1,
        allow_delegation=False
    )

    debug("✍️ Creating Writer")

    writer = Agent(
        role="Writer",
        goal="Create a concise and useful answer.",
        backstory="You are a clear technical writer.",
        llm=llm,
        verbose=False,
        max_iter=1,
        allow_delegation=False
    )

    debug("🔍 Creating Editor")

    editor = Agent(
        role="Editor",
        goal="Polish the response and improve clarity.",
        backstory="You are a precise technical editor.",
        llm=llm,
        verbose=False,
        max_iter=1,
        allow_delegation=False
    )

    # ========================================================
    # TASKS
    # ========================================================

    debug("📋 Creating Research task")

    research_task = Task(
        description=f"""
Analyze this task:

{user_task}

Identify 3-5 important points needed to answer it.
Do not write the final answer.
""",
        expected_output="3-5 concise research points.",
        agent=researcher
    )

    debug("📋 Creating Writing task")

    writing_task = Task(
        description=f"""
Answer this task:

{user_task}

Use the Researcher's analysis.
Write a concise answer of approximately 80-120 words.
""",
        expected_output="An 80-120 word answer.",
        agent=writer,
        context=[research_task]
    )

    debug("📋 Creating Editing task")

    editing_task = Task(
        description="""
Review the Writer's answer.

Improve clarity and structure.

Return ONLY the final polished answer.
""",
        expected_output="A polished final answer.",
        agent=editor,
        context=[research_task, writing_task]
    )

    # ========================================================
    # CREW
    # ========================================================

    debug("🔗 Creating sequential crew")

    crew = Crew(
        agents=[
            researcher,
            writer,
            editor
        ],
        tasks=[
            research_task,
            writing_task,
            editing_task
        ],
        process=Process.sequential,
        verbose=False,
        tracing=False
    )

    # ========================================================
    # EXECUTION
    # ========================================================

    for attempt in range(3):

        try:

            debug(
                f"⚡ Running crew "
                f"(attempt {attempt + 1}/3)"
            )

            # ------------------------------------------------
            # HIDE CREWAI TERMINAL OUTPUT
            # ------------------------------------------------

            captured_output = io.StringIO()

            with contextlib.redirect_stdout(captured_output):
                with contextlib.redirect_stderr(captured_output):

                    result = crew.kickoff()

            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            debug("🧠 Researcher completed")
            debug("✍️ Writer completed")
            debug("🔍 Editor completed")
            debug("✅ Crew execution completed")

            return str(result)

        except Exception as error:

            error_text = str(error).lower()

            rate_limit = (
                "rate limit" in error_text
                or "429" in error_text
                or "rate_limit_exceeded" in error_text
                or "tokens per minute" in error_text
            )

            if rate_limit:

                if attempt < 2:

                    wait = get_wait_time(
                        error,
                        attempt
                    )

                    debug(
                        f"⏳ Rate limit reached. "
                        f"Retrying in {wait:.1f}s"
                    )

                    time.sleep(wait)

                    continue

                debug("❌ Rate limit persisted")

                return demo_mode(user_task)

            debug(
                f"❌ CrewAI error: {error}"
            )

            return demo_mode(user_task)

    return demo_mode(user_task)


# ============================================================
# USER INTERFACE
# ============================================================

st.title("🤖 Agentic AI Crew")

st.markdown(
    "### Researcher → Writer → Editor"
)

st.write(
    "Give the AI crew a task and watch it produce the final answer."
)

st.divider()


# ============================================================
# INPUT
# ============================================================

user_task = st.text_area(
    "🎯 Enter your task",
    placeholder=(
        "Example: Explain quantum computing "
        "to a first-year engineering student."
    ),
    height=120,
    key="task_input"
)


# ============================================================
# RUN BUTTON
# ============================================================

run_button = st.button(
    "🚀 Run Task",
    type="primary",
    use_container_width=True
)


if run_button:

    if not user_task.strip():

        st.warning("Please enter a task first.")

    else:

        st.session_state.last_task = user_task

        with st.spinner(
            "🤖 Agents are working..."
        ):

            result = run_crew(
                user_task.strip()
            )

        st.session_state.final_output = result


# ============================================================
# FINAL OUTPUT
# ============================================================

if st.session_state.final_output:

    st.divider()

    st.subheader("✅ Final Output")

    st.markdown(
        st.session_state.final_output
    )


# ============================================================
# DEBUG SECTION
# ============================================================

if st.session_state.debug_logs:

    st.divider()

    debug_button = st.button(
        "🐛 Debug — Show Agent Workflow",
        use_container_width=True
    )

    if debug_button:

        st.subheader("🔧 Backend Activity")

        for message in st.session_state.debug_logs:

            st.markdown(
                f"`{message}`"
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CrewAI × Groq • Agentic AI Workshop"
)