import streamlit as st
from env.devops_env import DevOpsEnv
from tasks.easy_incident import TASK_EASY
from tasks.medium_incident import TASK_MEDIUM
from tasks.hard_incident import TASK_HARD
from inference import ai_agent_decision

# 1. Page Configuration
st.set_page_config(page_title="AIOps Control Plane", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for a more "User Friendly" Pro Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #3e4255; }
    code { color: #00ffc8 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Task Mapping
TASK_MAP = {
    "Easy: API Crash": TASK_EASY,
    "Medium: DB Auth Error": TASK_MEDIUM,
    "Hard: Traffic Flood": TASK_HARD
}

# 3. Initialize State
if 'env' not in st.session_state:
    st.session_state.env = DevOpsEnv(TASK_EASY)

# 4. Sidebar: Simulation Controls & Steps
with st.sidebar:
    st.title("🛠️ Control Center")
    selected_task = st.selectbox("Choose Scenario", list(TASK_MAP.keys()))
    
    if st.button("Reset / Load Selected Task", use_container_width=True):
        st.session_state.env = DevOpsEnv(TASK_MAP[selected_task])
        st.rerun()
    
    st.divider()
    st.subheader("📖 How to use:")
    st.markdown("""
    1. **Select** a scenario from the dropdown above.
    2. Click **Reset / Load Task** to initialize.
    3. **Analyze** the *System Logs* and *Metrics*.
    4. Click **'Let AI Fix It'** to trigger the agent.
    5. Watch the **Health Score** and **Logs** for recovery!
    """)
    st.info("The agent uses a logic-based priority system to resolve incidents.")

# 5. Main Dashboard Header
st.title("🛡️ AIOps Incident Command")
state = st.session_state.env.state_data

# 6. Service Metrics Row
cols = st.columns(len(state.services))
for i, (name, svc) in enumerate(state.services.items()):
    with cols[i]:
        # Logic for color-coding status
        color = "normal" if svc.status == "running" else "inverse"
        st.metric(
            label=name.upper(), 
            value=svc.status.upper(), 
            delta=f"{svc.error_rate*100}% Error", 
            delta_color=color
        )

st.divider()

# 7. Logs and Agent Action Section
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📟 System Logs")
    log_stream = "\n".join(state.logs[-10:])
    st.code(log_stream, language="bash")

with col_right:
    st.subheader("🤖 Agent Control")
    
    # Large Score Metric
    score = st.session_state.env.current_reward
    st.metric("System Health Score", f"{score:.2f}", help="Score increases as services recover and error rates drop.")
    
    if st.button("🚀 Let AI Fix It", type="primary", use_container_width=True):
        with st.status("Agent Analyzing Logs...", expanded=False) as status:
            action = ai_agent_decision(state.dict())
            st.write(f"**Reasoning:** {action.get('reasoning')}")
            # Step the environment
            new_state, reward, done, info = st.session_state.env.step(action)
            status.update(label="Action Executed!", state="complete", expanded=False)
        
        st.rerun()

    if st.button("Clear Logs", use_container_width=True):
        st.session_state.env.state_data.logs = ["Operator cleared logs."]
        st.rerun()