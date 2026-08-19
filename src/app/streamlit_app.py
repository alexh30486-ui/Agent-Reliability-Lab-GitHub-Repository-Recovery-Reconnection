import streamlit as st

st.set_page_config(
    page_title="Agent Reliability Lab",
    page_icon="🧪",
    layout="wide"
)

st.title("Agent Reliability Lab")
st.caption(
    "AI engineering evaluation platform for testing agent behavior, "
    "tool use, reasoning, and recovery."
)

st.divider()

# Overview
st.subheader("System Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Agents", "4")

with col2:
    st.metric("Evaluations", "0")

with col3:
    st.metric("Failure Types", "8")

with col4:
    st.metric("System Status", "READY")

st.divider()

# Agents
st.subheader("Agent Evaluation Pipeline")

agents = {
    "Research Agent": "Search → retrieve → summarize → answer",
    "Data Agent": "Question → SQL → database → analysis → answer",
    "Tool Agent": "Question → choose tool → execute → interpret",
    "File Agent": "Request → inspect file → extract → answer",
}

for agent_name, workflow in agents.items():

    with st.container(border=True):

        col1, col2, col3 = st.columns([1, 3, 1])

        with col1:
            st.write(agent_name)

        with col2:
            st.caption(workflow)

        with col3:
            if st.button(
                "Evaluate",
                key=f"evaluate_{agent_name}"
            ):
                st.session_state["selected_agent"] = agent_name


st.divider()

# Failure taxonomy
st.subheader("Failure Taxonomy")

failures = [
    "Hallucination",
    "Wrong tool",
    "Bad reasoning",
    "Incomplete task",
    "Malformed output",
    "Unnecessary tool call",
    "Failure to recover",
    "Safety violation",
]

cols = st.columns(4)

for index, failure in enumerate(failures):
    with cols[index % 4]:
        st.info(failure)

st.divider()

# Evaluation console
st.subheader("Evaluation Console")

selected_agent = st.session_state.get(
    "selected_agent",
    None
)

if selected_agent:

    st.success(
        f"{selected_agent} selected for evaluation."
    )

    st.write(
        "The evaluation engine will be connected here next. "
        "It will generate an agent trace, inspect the trace, "
        "and classify any reliability failures."
    )

else:

    st.info(
        "Select an agent above to begin an evaluation."
    )
